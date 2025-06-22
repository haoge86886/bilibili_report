from function import *
def main():
    print("输入想查找的关键词:")
    keyword = input()
    print("输入搜索深度")
    page = int(input())
    f = main_work(keyword,page)

    print("是否将结果发送至邮箱(y/n)")
    if input() == 'Y'or input() == 'y':
        from_email = input("输入发送者邮箱地址")
        host = input("输入邮箱主机地址")
        password = input("输入邮箱密码")
        to_email = input("输入邮箱接受者地址")

        email_send(keyword,from_email,password,f,to_email,host=host)
    else:
        exit(0)
if __name__ == '__main__':
    main()