from openai import OpenAI
import time
import json
import os
import sys
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)
sys.path.append(config['sys_path'])
from model import gpt_robot
from wxauto.wxauto import WeChat

os.chdir(os.path.dirname(__file__))#设置当前文件夹为工作目录

# 设置API密钥，若已经添加到环境变量中，可注释掉这一行
os.environ['OPENAI_API_KEY'] = config['openai_api_key']
wx = WeChat()

#创建一个人/群聊列表
human_group_info_list = config['human_group_info_list']

# name: 群组/人名称
# condition: 触发对话时，对方信息必须含有的关键词
# condition_type: 将对话输入给GPT时，是否需要过滤关键词，1为需要，0为不需要
# role_file: 角色配置路径
# pretrained_file: 预训练对话集路径



client = OpenAI()
gpt_models = config['gpt_models']
gpt_model = gpt_models[1]#选择模型


# 为每个群聊/人设计一个机器人,role为角色,pretrain是自己定义的预先对话
robot_group_array=[]#机器人列表
for human_group_info in human_group_info_list:
	wx.AddListenChat(who=human_group_info['name'], savepic=False)  
	robot=gpt_robot.Robot(human_group_info,client,model=gpt_model)
	robot_group_array.append(robot)

wait = 10#设置接收时间间隔,若设置太短容易使程序频繁拉取信息的过程中漏掉某些信息

while True:
	msgs = wx.GetListenMessage()#获取所有聊天信息
	for robot in robot_group_array:
		robot.chat(msgs)
	time.sleep(wait)
