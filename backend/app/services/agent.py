import asyncio
import logging
from datetime import datetime
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, status
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.models.message import Message
import utilities.config as config

router = APIRouter()
logger = logging.getLogger(__name__)


async def process_llm(
    prompt: str, session_id: int, db: Session, context: str = ""
) -> AsyncGenerator[str, None]:
    """LLMの処理を行い、チャンクされたメッセージを返すジェネレータ関数

    Args:
        prompt (str): ユーザーのメッセージ
        context: 会話の文脈

    Yields:
        str: LLMによって生成されたメッセージ
    """
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.5,
        streaming=True,
        openai_api_key=config.OPENAI_API_KEY,
    )
    # System prompt with specified requirements
    system_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                """
            # Adaptive Engineering Analysis Framework

            ## Examples for Dynamic Response Generation

            ### Example 1: Response Structure for Questions about LLM (Large Language Models)

            # What is an LLM?

            ## Overview
            - An LLM (Large Language Model) is an AI model pre-trained on vast amounts of text data
            - Capable of performing natural language processing tasks at a high level

            ## Detailed Explanation
            - A large-scale neural network based on deep learning
            - Complex models with billions to trillions of parameters
            - Based on the Transformer architecture

            ## Use Cases
            - Natural language generation
            - Text translation
            - Code completion
            - Question-answering systems
            - Content creation assistance

            ### Example 2: Response Structure for Code Analysis

            # Code Analysis Report

            ## Overview
            - Comprehensive technical analysis of the provided code
            - Evaluation of system architecture and implementation strategies

            ## Code Explanation
            - Overall structure and design principles of the code
            - Identification of key technical approaches
            - Strengths and weaknesses of the implementation

            ## Function Explanation
            - Role and responsibility scope of each function
            - Algorithm efficiency
            - Performance characteristics

            ## Modification Proposal

            # Improved Code Snippet
            def optimized_function(params):
                # Optimized implementation
                pass

            ## Further Suggestions
            - Scalability of the architecture
            - Security enhancements
            - Performance tuning

            ### Example 3: Response Structure for Explaining Technical Concepts

            # Understanding Blockchain Technology

            ## Introduction
            - Blockchain is a decentralized ledger technology
            - Enables secure and transparent peer-to-peer transactions

            ## Key Features
            - **Immutability**: Once data is recorded, it cannot be altered
            - **Decentralization**: No central authority controlling the network
            - **Transparency**: Transactions are visible to all participants

            ## How It Works
            - Transactions are grouped into blocks
            - Each block is linked to the previous one using cryptography
            - Consensus mechanisms validate new blocks (e.g., Proof of Work)

            ## Applications
            - Cryptocurrencies like Bitcoin and Ethereum
            - Supply chain management
            - Smart contracts
            - Voting systems

            ## Guidelines for Dynamic Structure Generation
            1. Thoroughly analyze the input context.
            2. Dynamically select the optimal response structure.
            3. Express the response directly without wrapping it in code blocks.
            4. Prioritize technical insight and clarity.

            ## Criteria for Structural Adaptation
            - Complexity of the question
            - Required depth of technical detail
            - Specificity of the context
            - User's intent

            ## Final Instructions
            - Generate the most appropriate and insightful analytical structure.
            - **Do not include ```markdown at the beginning of the response.**
            - Maximize clarity, accuracy, and relevance.
            - Adapt to the unique characteristics of the input context.
            """
            ),
            HumanMessagePromptTemplate.from_template(
                "Context Analysis:\n{context}\n\nEngineer's Adaptive Task: {prompt}"
            ),
        ]
    )

    chain = system_template | llm

    res = chain.astream({"prompt": prompt, "context": context})
    full_response = ""
    accumulated_content = ""
    chunk_size = 25
    last_send_time = asyncio.get_event_loop().time()
    time_threshold = 1.0
    try:
        async for chunk in res:
            content = chunk.content if hasattr(chunk, "content") else str(chunk)
            full_response += content
            accumulated_content += content

            current_time = asyncio.get_event_loop().time()
            if (
                len(accumulated_content) >= chunk_size
                or (current_time - last_send_time) >= time_threshold
            ):
                yield accumulated_content
                accumulated_content = ""
                last_send_time = current_time
    except Exception as e:
        logger.error(f"Error during LLM processing: {str(e)}")
        yield f"Error: {str(e)}"

    if accumulated_content:
        yield accumulated_content

    logger.info(f"LLM full response: {full_response}")

    if full_response:
        user_message = Message(
            session_id=session_id,
            content=prompt,
            is_user=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        agent_message = Message(
            session_id=session_id,
            content=full_response,
            is_user=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        try:
            db.add(user_message)
            db.add(agent_message)
            db.commit()
            db.refresh(user_message)
            db.refresh(agent_message)
        except SQLAlchemyError as db_error:
            db.rollback()
            logger.error(
                f"Database error while saving messages for session {session_id}: {str(db_error)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error while saving messages for session {session_id}: {str(db_error)}",
            )
        except Exception as e:
            db.rollback()
            logger.error(
                f"Unexpected error while saving messages for session {session_id}: {str(e)}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error while saving messages for session {session_id}: {str(e)}",
            )
