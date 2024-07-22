import re
import streamlit as st
import pandas as pd

if "rag_change_flag" not in st.session_state:
    st.session_state["rag_change_flag"] = 0

if "tool_change_flag" not in st.session_state:
    st.session_state["tool_change_flag"] = 0


def get_prompt_content_var(prompt_content):
    # 正则表达式模式，用于匹配大括号中的内容
    pattern = r"\{(.*?)\}"
    # 使用 re.findall 查找所有匹配项
    matches = re.findall(pattern, prompt_content)
    # 输出所有匹配项
    table = []
    for key in matches:
        # 生成列表
        table.append({"command":key,"rating":""})
    return table

def prompt_format(prompt_content,values):
    # 创建一个字典用于替换
    replace_dict = {item['key']: item['value'] for item in values}
    # 使用 str.format_map 进行替换
    output_str = prompt_content.format_map(replace_dict)
    return output_str

@st.experimental_dialog("Agent编排规则")
def vote(text):
    st.write(text)
    if st.button("确定"):
        st.rerun()

# 左边布局
with st.sidebar:
    st.title("👏欢迎使用Agent应用编排功能🎆")
    st.divider()
    st.session_state["messages"] = []
    # # 获取多个预设提示词
    # st.page_link("pages/prompt_index.py",label="提示词管理页面",icon="🌍")

    # # 开始调用接口
    # prompt_info_list = send_get("http://127.0.0.1:8080/prompt/list")
    # prompt_value = ""
    # if prompt_info_list['code'] == 200:
    #     prompt_list = prompt_info_list['data']
    #     prompt_values = []
    #     for prompt in prompt_list:
    #         prompt_values.append(prompt['prompt_context'])
    #     prompt_value = st.selectbox("请选择预设提示词:",prompt_values,index=None)

    prompt_content = st.text_area("对话前提示词：",placeholder="""您可以设置提示词约束Al回复效果，最简单的公式是：角色设定 + 期望目标＋回复形式。例如：
    你是一个行政助手，我希望你能为我提供员工行为规范，请用严肃的方式表达。
    您也可以通过“自定义提示词”组装提示词，为您生成提示词成品预览。""",value="")
    st.write("提示词用于对 Al 的回复做出一系列指令和约束。可插入表单变量，如{input}。这段提示词不会被最终用户所看到")
    st.session_state["system"] = []

    if prompt_content:
        table = get_prompt_content_var(prompt_content)
        if len(table) > 0:
            df = pd.DataFrame(
                table
            )
            edited_df = st.data_editor(
                df,
                column_config={
                    "command": "Key",
                    "rating": st.column_config.TextColumn(
                        "Value",
                        help="请输入目前key的对应value"
                    )
                },
                disabled=["command"],
                hide_index=True,
            )
            # 提示词这里加入system角色的提示词
            var_max_range = edited_df["command"].idxmin()
            if prompt_content and var_max_range>=0:
                values=[]
                for i in range(0, var_max_range + 1):
                    command = edited_df.loc[i]["command"]
                    rating = edited_df.loc[i]["rating"]
                    # print(command)
                    # print(rating)
                    if command and rating:
                        values.append({"key":command,"value":rating})
                if len(values) > 0:
                    st.session_state["system"].append({"role": "human", "content": prompt_format(prompt_content,values)})
                    st.session_state["system"].append({"role": "ai", "content": "好的"})

    st.divider()

    files = st.file_uploader("挂载企业知识库",accept_multiple_files=True,type=["pdf","txt"])

    if files:
        chain_type = st.selectbox("请选择RAG提交策略:", ["stuff", "map-reduce", "refine", "map-rerank"])
        if "rag_change_flag" in st.session_state and st.session_state["rag_change_flag"] == 0:
            st.session_state["rag_change_flag"] = 1
            st.session_state["history"] = []
            vote("第一次添加文档，将重置所有的对话记忆")
    else:
        if "rag_change_flag" in st.session_state and st.session_state["rag_change_flag"] == 1:
            st.session_state["rag_change_flag"] = 0
            st.session_state["history"] = []
            vote("取消所有的文档，将重置所有的对话记忆")

    st.divider()

    tool_names = st.multiselect("请选择使用工具:",["天气查询工具","自定义SQLite数据库工具"])
    if tool_names:
        print("工具调用中.....")

        print("tool_change_flag" in st.session_state)

        if "tool_change_flag" in st.session_state and st.session_state["tool_change_flag"] == 0:
            print("第一次添加工具")
            st.session_state["tool_change_flag"] = 1
            st.session_state["history"] = []
            vote("第一次添加工具，将重置所有的对话记忆")
    else:
        if "tool_change_flag" in st.session_state and st.session_state["tool_change_flag"] == 1:
            print("删除完工具")
            st.session_state["tool_change_flag"] = 0
            st.session_state["history"] = []
            vote("取消所有的工具，将重置所有的对话记忆")


    st.divider()

    content_flag = st.radio("请选择是否需要开场白:",["是","否"],index=1)

    if content_flag == "是":
        df_few = pd.DataFrame(
            [
                {"command": "", "rating": ""}
            ]
        )

        edited_df_few = st.data_editor(
            df_few,
            column_config={
                "command": "角色（ai，human）",
                "rating": st.column_config.TextColumn(
                    "content",
                    help="内容"
                )
            },
            hide_index=True,
            num_rows="dynamic"
        )
        max_range = edited_df_few.shape[0]
        if max_range >= 0:
            for i in range(max_range):
                command = edited_df_few.loc[i]["command"]
                rating = edited_df_few.loc[i]["rating"]
                if command and rating:
                    st.session_state["messages"].append({"role":command,"content":rating})
                    # st.session_state["history"] = []

# 右边布局
with st.container():
    col1, col2= st.columns(2)
    with col1:
        st.markdown("### ➡️AI问答框⬇️")
    with col2:
        with st.popover("模型配置⬇️"):
            open_ai_key = st.text_input("输入模型密钥:",type="password")
            api_base = st.text_input("请输入密钥搭配base_url,若无则无需填写")
            model_name = st.selectbox("欢迎来到模型的选择页面,请选择你想选择的模型:👋",
                                      ['gpt-3.5-turbo', 'gpt-4o', 'gpt-4-turbo'])
            if model_name:
                # 进行模型配置
                temperature = st.slider("temperature:", min_value=0.0, max_value=2.0, step=0.1,value=1.0)
                max_tokens = st.number_input("max_tokens:", min_value=50, max_value=600, step=1,value=200)

# 生成聊天页面
st.divider()

history_messages = []

if "history" in st.session_state:
    history_messages.extend(st.session_state["history"])
# if "messages" in st.session_state:
#     history_messages.extend(st.session_state["messages"])
print(history_messages)
for message in history_messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

# 聊天页面,根据历史记录生成初始聊天记录
input = st.chat_input("请输入你的问题")
if "history" not in st.session_state:
    st.session_state["history"] = []

if input :
    # 输入类型先展示
    with st.chat_message("human"):
        st.write(input)
    # 整合完整的记忆
    memory = []
    if "system" in st.session_state:
        memory.extend(st.session_state['system'])
    if "messages" in st.session_state:
        memory.extend(st.session_state['messages'])
    if "history" in st.session_state:
        memory.extend(st.session_state['history'])
    # print(memory)
    rag_flag = False
    if files:
        rag_flag = True
    else:
        chain_type = None
    # 进行模型调用
    with st.spinner("AI正在思考中，请等待....."):
        # response = get_agent_response(open_ai_key,model_name,temperature,max_tokens,api_base,memory,input,tool_names,rag_flag,files,chain_type)
        # 展示模型输入
        # with st.chat_message("ai"):
            # st.write(response)
        # 将模型调用结果和用户输入一起放入历史记录
        if "history" in st.session_state:
            st.session_state["history"].append({"role": "human", "content": input})
            # st.session_state["history"].append({"role": "ai", "content": response})













