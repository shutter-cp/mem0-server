# 项目概述
Memory Service API 是一个基于 Flask 框架的轻量级 Web 服务，用于 mem0 存储、检索、搜索、更新、删除和管理内存（Memories）。这个服务可以用于多种应用场景，例如个人助理、知识管理、数据跟踪或用户行为存储。通过一组简单的 API，你可以对用户的记忆进行全生命周期的管理，包括存储、检索、历史记录查询等。

该项目设计简洁，易于扩展和维护，适用于需要快速开发内存管理功能的场景。

## 核心功能
### 存储内存
存储用户的记忆信息，例如个人的喜好、事件或行为数据，并可以附加元数据进行分类。
### 检索内存
支持检索所有内存或根据内存 ID 获取特定的内存内容。
### 搜索内存
支持根据查询条件对内存进行搜索，并可以根据用户 ID 限制搜索范围，帮助找到相关记忆。
### 更新内存
支持对已经存储的内存进行更新，并记录每次更新的历史。
### 内存历史记录
提供接口查询特定内存的历史版本，便于追踪内存的变化。
### 删除内存
可以删除特定的内存或删除某个用户的所有内存数据。
### 重置内存
清空所有内存数据和历史记录，适用于重置系统或清除数据的场景。

## 安装方式
1. 修改配置，openai_key 或者 ollama配置
```shell
cp env .env
```

2. 构建镜像
```shell
docker build -t mem0:0.1 .
```

3. 启动服务
> 应该使用healthcheck的，没有时间调试，暂时使用两次命令来启动
```shell
docker compose up -d qdrant
docker compose up -d mem0
```


```yaml
openapi: 3.0.0
info:
  title: Memory Service API
  version: 1.0.0
  description: API for managing memory operations such as storing, retrieving, updating, and deleting memories.

paths:
  /memory/add:
    post:
      summary: Store a memory
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: string
                  description: Memory data to store
                user_id:
                  type: string
                  description: User ID for whom the memory is stored
                metadata:
                  type: object
                  description: Optional metadata for the memory
      responses:
        201:
          description: Memory added successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  result:
                    type: string
                    description: Memory ID of the stored memory

  /memory/get_all:
    post:
      summary: Retrieve all memories
      responses:
        200:
          description: All stored memories
          content:
            application/json:
              schema:
                type: object

  /memory/get:
    post:
      summary: Retrieve a specific memory by ID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                memory_id:
                  type: string
                  description: The ID of the memory to retrieve
      responses:
        200:
          description: The requested memory
          content:
            application/json:
              schema:
                type: object

  /memory/search:
    post:
      summary: Search for memories based on a query
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
                  description: The query to search for
                user_id:
                  type: string
                  description: The user ID to restrict the search
      responses:
        200:
          description: Related memories
          content:
            application/json:
              schema:
                type: object

  /memory/update:
    post:
      summary: Update a specific memory by ID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                memory_id:
                  type: string
                  description: The ID of the memory to update
                data:
                  type: string
                  description: The new data to update the memory with
      responses:
        200:
          description: Memory updated successfully
          content:
            application/json:
              schema:
                type: object

  /memory/history:
    post:
      summary: Retrieve the update history of a specific memory by ID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                memory_id:
                  type: string
                  description: The ID of the memory to retrieve the history for
      responses:
        200:
          description: The memory's update history
          content:
            application/json:
              schema:
                type: object

  /memory/delete:
    post:
      summary: Delete a specific memory by ID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                memory_id:
                  type: string
                  description: The ID of the memory to delete
      responses:
        200:
          description: Memory deleted successfully
          content:
            application/json:
              schema:
                type: object

  /memory/delete_all:
    post:
      summary: Delete all memories for a specific user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: string
                  description: The user ID to delete all memories for
      responses:
        200:
          description: All memories for the user deleted successfully
          content:
            application/json:
              schema:
                type: object

  /memory/reset:
    post:
      summary: Reset all memories and history
      responses:
        200:
          description: All memories and history reset successfully
          content:
            application/json:
              schema:
                type: object

components:
  schemas:
    Memory:
      type: object
      properties:
        data:
          type: string
        user_id:
          type: string
        metadata:
          type: object


```