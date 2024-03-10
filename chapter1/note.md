# Chapter1. OpenAI API 入門

## 為什麼不直接使用，而要串接 OpenAI API ?

- 流程自動化
- 客製化聊天內容
- 延伸聊天範圍
- 整合 AI 功能

## 註冊 OpenAI API 帳戶

- [OpenAI developer platform](https://platform.openai.com/)
- [Playground - OpenAI API](https://platform.openai.com/playground)

## 利用 Playground 熟悉 API

> 注意：在 Playground 上使用功能也都會計價！

### API 類型如下

| Mode | Description |
| -------- | -------- |
| chat     | 由程式以**結構化的訊息串**來提供對答過程給模型作為提示（prompt），API 可以根據過往的回覆脈絡回覆相關的內容。 |
| completion | 由程式提供一段話作為**提示**，API 會回覆一段可以接續的文字。 |

### 此書採用的模型為

1. gpt-3.5-turbo
2. gpt-4

### 命名規則

1. 若模型後面有**日期**，則表示模型最後訓練的時間，可能有額外加上新功能，但訓練資料仍到2021年9月
2. 若名稱有「Xk」，如：4k, 16k，代表模型可處理的 token 數量
3. 沒有標示日期，表示為**穩定版**

### 認識 chat 模式的三種角色

1. system: 這部分主要是描述模型所要扮演的特性
2. user: 與 AI 對答的使用者
3. assistant: 回覆使用者的 AI

> 注意：AI 不會自動記錄聊天過程，送出訊息前需要將先前的對話內容一併傳回，才能維持脈絡。因此對話越長越龐大時，token 數量也會越多，費用也越高！

## 重點摘要

- 程式發送給 API 訊息附帶的文字為「提示（prompt）」，訊息是由這兩個部分組成
  1. 發言角色（user, assistant）所組成
  2. 發言內容
- 若要讓 AI 能夠維持相同的對話脈絡，需要將所有對話過程一併傳回給 API