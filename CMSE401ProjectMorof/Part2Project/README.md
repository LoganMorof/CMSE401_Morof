# Software Abstract
This software example demonstrates the use of Python for real-time cryptocurrency price tracking utilizing asynchronous programming (asyncio) in combination with asynchronous HTTP requests (aiohttp). Specifically, this example leverages the CoinMarketCap API to fetch cryptocurrency prices concurrently, significantly reducing the total retrieval time compared to sequential fetching methods.

## What is this Software?
The Crypto Portfolio Price Tracker is an example of application-level software leveraging modern asynchronous programming techniques. It integrates Python's built-in concurrency framework (asyncio) with the efficient asynchronous HTTP client library (aiohttp) to create a robust and high-performance API request handler.

The primary functions of this software include:

- Fetching real-time cryptocurrency prices concurrently.
- Displaying retrieved price data clearly and succinctly in a command-line environment.
- Demonstrating how asynchronous methods can significantly improve efficiency when interacting with web-based APIs.

## Applications in Science and Engineering
This type of software is highly relevant across multiple fields in science, engineering, and especially finance and data science, due to its capability to handle extensive real-time data efficiently.

Specific Applications Include:

Financial Analysis & Trading Systems:
- Utilized in algorithmic trading to rapidly process and analyze financial data for arbitrage detection and real-time price monitoring.

Data Engineering and Science:
- Essential for efficiently fetching and aggregating large datasets, particularly from web-based sources, for immediate analytical processing and machine learning applications.

Real-Time Systems and Dashboards:
- Commonly used for creating real-time visualization dashboards, alert systems, or decision-support tools in scientific research, IoT monitoring, and engineering analytics.

## Software Type
This software can be categorized as an application-level programming tool, which serves as an efficient wrapper around external API services. It simplifies the complex task of concurrent network operations, abstracting away intricate management of parallel HTTP requests through simple and maintainable Python code.

Software Layers & Roles:

- API Layer (CoinMarketCap API): Provides comprehensive real-time cryptocurrency market data.
- Middleware Layer (aiohttp): Handles asynchronous network communication and HTTP management.
- Programming Framework (asyncio): Coordinates and schedules concurrent tasks for optimized performance.
- Application Layer (Python Script): Provides an intuitive interface for users to fetch and interact with real-time crypto prices effectively.

# Instilation Instructions
