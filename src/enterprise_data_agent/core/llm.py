import torch
from transformers import AutoProcessor, AutoModelForImageTextToText, BitsAndBytesConfig
from enterprise_data_agent.config import MODEL_ID, USE_4BIT, MAX_NEW_TOKENS

class LLMEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMEngine, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        print(f"[System] Initializing LLM Engine ({MODEL_ID})...")
        bnb_cfg = None
        if USE_4BIT:
            bnb_cfg = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
            )
        
        self.processor = AutoProcessor.from_pretrained(MODEL_ID, trust_remote_code=True)
        self.model = AutoModelForImageTextToText.from_pretrained(
            MODEL_ID, quantization_config=bnb_cfg, device_map="auto", trust_remote_code=True
        ).eval()
        print("[System] LLM Ready.")

    def generate(self, system_prompt: str, context: str, user_input: str) -> str:
        """
        Generic generation function suitable for Qwen chat template.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"History:\n{context}\n\nCurrent Task: {user_input}"}
        ]
        
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.processor(text=[text], padding=True, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs, max_new_tokens=MAX_NEW_TOKENS, temperature=0.3
            )
            
        generated_ids = [
            output_ids[len(input_ids):] 
            for input_ids, output_ids in zip(inputs.input_ids, generated_ids)
        ]
        return self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
