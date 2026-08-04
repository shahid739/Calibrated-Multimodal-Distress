#!/usr/bin/env python
"""
Data Preparation Script for DERS-X
"""

import os
import argparse
from datasets import load_dataset
from transformers import DistilBertTokenizerFast, Wav2Vec2Processor


def main():
    parser = argparse.ArgumentParser(description="Prepare IEMOCAP data")
    parser.add_argument("--dataset", type=str, default="AbstractTTS/IEMOCAP")
    parser.add_argument("--split", type=str, default="train")
    args = parser.parse_args()

    # Load dataset
    print(f"Loading dataset: {args.dataset}")
    ds = load_dataset(args.dataset, split=args.split)
    print(f"Dataset size: {len(ds)}")

    # Load tokenizers
    text_tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
    audio_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")

    # Display sample
    sample = ds[0]
    print(f"Sample keys: {sample.keys()}")
    print(f"Transcription: {sample['transcription'][:100]}...")
    print(f"Emotion: {sample.get('major_emotion', 'N/A')}")
    print(f"Activation: {sample.get('EmoAct', 'N/A')}")

    # Tokenize text sample
    tokens = text_tokenizer(sample.get("transcription", ""), truncation=True, max_length=128)
    print(f"Text tokens: {len(tokens['input_ids'])}")

    print("Data preparation complete!")


if __name__ == "__main__":
    main()