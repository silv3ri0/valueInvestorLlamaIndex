import os
from dotenv import load_dotenv
import asyncio
import nest_asyncio
import requests
import sys
import logging
from llama_index.core.agent.workflow import AgentWorkflow, ReActAgent
from llama_index.core.llms import CustomLLM, LLMMetadata
from llama_index.core.llms import CompletionResponse
from llama_index.core.llms.callbacks import llm_completion_callback
from typing import Any
from tools.data_fetcher import fetch_financial_data
from tools.metrics import calculate_metrics
from tools.valuation import estimate_intrinsic_value, evaluate_company

# Configure logging (console only)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Set console encoding to UTF-8 (Windows only)
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables from .env file
load_dotenv()

# Apply nest_asyncio to handle async calls
nest_asyncio.apply()

# Verify DeepSeek API key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    raise ValueError("DeepSeek API key not configured. Add it to the .env file or environment variables.")


# --- DeepSeek LLM class compatible with llama-index ---
class DeepSeekLLM(CustomLLM):
    model_name: str = "deepseek-chat"

    def __init__(self, model_name: str = "deepseek-chat"):
        super().__init__()
        self.model_name = model_name

    def complete(self, prompt: str, **kwargs) -> CompletionResponse:
        """Call the DeepSeek API to get a response."""
        api_key = os.getenv("DEEPSEEK_API_KEY")
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system",
                 "content": "You are a value investing expert like Warren Buffett. Provide a concise evaluation in English based on the data provided, without recalculating any values."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 512,
            "temperature": 0.7
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            text = response.json()["choices"][0]["message"]["content"]
            return CompletionResponse(text=text)
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> Any:
        """Simulate streaming by yielding the full result as a single chunk."""
        response = self.complete(prompt, **kwargs)
        yield CompletionResponse(text=response.text)

    @property
    def metadata(self) -> LLMMetadata:
        """Return model metadata as LLMMetadata."""
        return LLMMetadata(
            context_window=4096,
            num_output=512,
            model_name=self.model_name
        )


# --- Configure DeepSeek LLM ---
llm = DeepSeekLLM(model_name="deepseek-chat")

# --- Create agents ---
extractor_agent = ReActAgent(
    name="extractor_agent",
    description="Extracts quantitative financial data from yfinance.",
    system_prompt="You are an assistant that collects financial data from yfinance.",
    tools=[fetch_financial_data],
    llm=llm,
)

analyst_agent = ReActAgent(
    name="analyst_agent",
    description="Calculates value investing metrics and intrinsic value.",
    system_prompt="You are an assistant that calculates P/E, P/B, ROE, and intrinsic value using the DCF model from estimate_intrinsic_value.",
    tools=[calculate_metrics, estimate_intrinsic_value],
    llm=llm,
)

valuator_agent = ReActAgent(
    name="valuator_agent",
    description="Evaluates whether a company is undervalued or overvalued.",
    system_prompt="You are an assistant that evaluates companies like Warren Buffett based on provided data. Respond in English.",
    tools=[evaluate_company],
    llm=llm,
)

# --- Create workflow ---
workflow = AgentWorkflow(
    agents=[extractor_agent, analyst_agent, valuator_agent],
    root_agent="extractor_agent",
)


# --- Async function to run the workflow ---
async def run_workflow(ticker: str) -> str:
    # Fetch data explicitly
    data = fetch_financial_data(ticker)
    logger.info(f"Raw data fetched for {ticker}: {data}")

    # Calculate metrics and intrinsic value explicitly
    metrics = calculate_metrics(data)
    intrinsic_value = estimate_intrinsic_value(data)
    logger.info(f"Intrinsic value calculated for {ticker}: {intrinsic_value}")

    # Ensure correct dividend yield
    metrics["dividend_yield"] = data["dividend_yield"]

    # Evaluate explicitly
    evaluation = evaluate_company(metrics, intrinsic_value, data["price"], data["market_cap"])
    logger.info(f"Evaluation data for {ticker}:\n{evaluation}")

    # Get agent response and extract text
    agent_response = await valuator_agent.run(
        user_msg=f"Is {ticker} undervalued? Here is the evaluation data:\n{evaluation}")
    response_text = agent_response.text if hasattr(agent_response, 'text') else str(agent_response)

    return evaluation + "\n\n" + response_text


# --- Execute the workflow ---
if __name__ == "__main__":
    ticker = "BC.MI"  # Fixed ticker for Brunello Cucinelli (Milan)
    try:
        logger.info(f"Starting analysis for {ticker}")
        response = asyncio.run(run_workflow(ticker))
        print(f"Response for {ticker}:\n{response}")
        # Save results to a file with UTF-8 encoding
        with open(f"analysis_{ticker}.txt", "w", encoding="utf-8") as f:
            f.write(f"Response for {ticker}:\n{response}")
        logger.info(f"Analysis completed for {ticker}")
    except Exception as e:
        logger.error(f"Error during analysis of {ticker}: {e}")
        print(f"Error: {e}")