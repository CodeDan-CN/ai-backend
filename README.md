 # 基础功能迭代计划

 1. 提示词管理模块
 2. milvus存储功能
 3. milvus搜索功能
 4. langchain 自定义retriever
 5. 构建带记忆体的v2版本rag
 6. 部署发布云服务器，实现手机端访问，方便我进行英语的沟通与学习

预计迭代完成时间7.28日

## 后端详细需求分析
1. 文件组管理（新增文件组，修改文件组，删除文件组，修改文件组）(☑️)
2. 文件上传功能，文件组文件预览列表（☑️）
3. 文件切割预览()
4. embedding功能
5. milvus向量数据库存入
6. 构建RAG Chain（langchain 自定义retriever，构建带记忆体的v2版本rag）

## 前端详细需求分析
1. 文件组管理页面，文件上传按钮
2. 文件切割方式选择页面，文件切割预览页面
3. 文件embedding页面
4. agent编排中可自由选择文件组

## 后端详细设计
1. 文件组数据字段（id,group_name,create_time）
2. 文件上传记录表（id,file_name,file_type,group_id,create_time）
3. milvus字段（id,pk,text,vector,group_id）







### 二期迭代计划
1. 调研文字转语音，实现语音交互功能
2. 调研orm技术，实现截图to记录进行存储，而不是手动倒入文件

预计迭代完成时间8.04
