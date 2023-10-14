import random

soup_pref = input('吃辣嗎？（Yes請輸入1，No請輸入0）: ')
soup_choice = random.randint(0, 3)

option = ['四川麻辣', '原味昆布', '牛奶起司', '東北酸菜']

if soup_pref == '1':
    print('湯底選：', option[soup_choice])
    
elif soup_pref == '0':
    non_spicy_choice = random.randint(0, 3)
    print('湯底選：', option[non_spicy_choice])

else:
    print('請輸入0或1')