import json
from operator import itemgetter


#  返回品牌名列表以及品牌下车系数量列表
def part_rand_series(rand_num, total_mes):
    # for i in rand_name:
    #     rand_mes = {'车系数量': str(j) for j in re.findall("\d+\.?\d*", i)}
    #     json_data["".join(re.findall(r'[\u4e00-\u9fa5a-zA-Z]', i))] = eval(rand_mes['车系数量'])
    new_sys = sorted(rand_num.items(), key=lambda d: d[1], reverse=False)  # 根据车系数量排序
    new_part = new_sys  # 需要截取片段时可使用
    part_rand_name = list(map(itemgetter(0), new_part))
    part_rand_num = list(map(itemgetter(1), new_part))

    # 生成对应的json文件
    # jsontext = {"car_name": part_rand_name, "car_num": part_rand_num}
    # jsondata = json.dumps(jsontext, indent=4, separators=(',', ': '), ensure_ascii=False)
    # f = open("static/gra_one_data.json", 'w', encoding='utf-8')
    # f.write(jsondata)
    # f.close()

    return part_rand_name, part_rand_num


#  读取文本返回列表
def read(src):
    with open(src, 'r', encoding="utf-8") as f:
        text = f.readlines()
        f.close()

    # 删除停售的车辆信息
    new_text = []
    for i in text:
        if "停售" in i:
            pass
        else:
            split_i = i.split("*")
            new_text.append(split_i)

    return new_text


#  返回第一个车系数量分布图需要的数据
def gra_one(new_text):
    rand_name = []
    total_mes = []
    for i in new_text:
        json_data = {'品牌': i[1], '车系': i[2][:-9], '评分': i[2][-4:], '马力': i[4], '车款': i[6], '价格': i[7]}
        rand_name.append(i[1])
        total_mes.append(json_data)

    rand_num = {}
    for i in total_mes:
        if i['品牌'] in rand_num.keys():
            rand_num[i['品牌']] = rand_num[i['品牌']] + 1
        else:
            rand_num[i['品牌']] = 1

    return rand_num, total_mes


#  返回车系对应的评分
def car_score(total_mes):
    new_total_mes = []
    for i in total_mes:
        if "暂无" not in i["评分"]:
            new_total_mes.append(i)

    car_name = []
    car_sc = []
    for i in new_total_mes:
        if i["车系"] not in car_name:
            car_name.append(i["车系"])
            car_sc.append(i["评分"])

    # 生成对应的json文件
    # jsontext = {"car_name": car_name, "car_score": car_sc}
    # jsondata = json.dumps(jsontext, indent=4, separators=(',', ': '), ensure_ascii=False)
    # f = open("static/score_line.json", 'w', encoding='utf-8')
    # f.write(jsondata)
    # f.close()

    return car_name, car_sc


# 返回用户评论数量饼图所需的数据
def command_mes(new_text):
    re_text = []
    for i in new_text:
        if i[8] == "暂无口碑数据\n":
            continue
        re_text.append(i[8])

    # 生成对应的json文件
    # jsontext = {"recommand": list(eval(re_text[0]).keys()), "re_num": list(eval(re_text[0]).values())}
    # jsondata = json.dumps(jsontext, indent=4, separators=(',', ': '), ensure_ascii=False)
    # f = open("static/command.json", 'w', encoding='utf-8')
    # f.write(jsondata)
    # f.close()

    return list(eval(re_text[0]).keys()), list(eval(re_text[0]).values())
    # print(type(re_text))
    # print(len(re_text))
    # for i in range(30):
    #     print(re_text[i])


# 返回车款马力数据
def car_para(total_mes):
    new_para = []
    for i in total_mes:
        if "车型" in i["马力"] or "参数配置未公布" in i["马力"]:
            continue
        new_para.append(i["马力"])


# 返回车动力方式数量数据
def power_type(total_mes):
    power_total = {"涡轮增压+电动增压": 0, "双涡轮增压": 0, "涡轮增压": 0, "发动机+电动机": 0, "电动机": 0, "发动机": 0}
    for i in total_mes:
        if '参数配置未公布' not in i["马力"] and "型" not in i["马力"]:
            if "涡轮增压" in i["马力"]:
                if "双涡轮增压" in i["马力"]:
                    power_total["双涡轮增压"] = power_total["双涡轮增压"] + 1
                elif "电动增压" in i["马力"]:
                    power_total["涡轮增压+电动增压"] = power_total["涡轮增压+电动增压"] + 1
                else:
                    power_total["涡轮增压"] = power_total["涡轮增压"] + 1
            elif "电动" in i["马力"]:
                if "发动机" in i["马力"]:
                    power_total["发动机+电动机"] = power_total["发动机+电动机"] + 1
                else:
                    power_total["电动机"] = power_total["电动机"] + 1
            else:
                power_total["发动机"] = power_total["发动机"] + 1

    # 生成对应的json文件
    # gra_need_data = []
    # for i in power_total.keys():
    #     dict = {"name": i, "value": power_total[i]}
    #     gra_need_data.append(dict)
    #
    # jsontext = {"power_name": list(power_total.keys()), "power_total": gra_need_data}
    #
    # jsondata = json.dumps(jsontext, indent=4, separators=(',', ': '), ensure_ascii=False)
    # f = open("static/power_type.json", 'w', encoding='utf-8')
    # f.write(jsondata)
    # f.close()
    return power_total


# 返回同一车系下不同车款的价格曲线
def car_price(total_mes):
    new_car_price = {}
    for i in total_mes:
        if "暂无报价" in i["价格"]: continue
        if i["车系"] not in new_car_price.keys():
            a = [i["价格"]]
            new_car_price[i["车系"]] = a
        else:
            new_car_price[i["车系"]].append(i["价格"])
    for i in new_car_price.keys():
        new_car_price[i] = (min(new_car_price[i])[:-2], max(new_car_price[i])[:-2])

    car_price_name = list(new_car_price.keys())
    car_price_mami = list(new_car_price.values())

    # 生成对应的json文件
    # jsontext = {"car_name": list(new_car_price.keys()),
    #             "car_price_max": list(map(itemgetter(0), car_price_mami)),
    #             "car_price_min": list(map(itemgetter(1), car_price_mami))
    #             }
    #
    # jsondata = json.dumps(jsontext, indent=4, separators=(',', ': '), ensure_ascii=False)
    # f = open("static/car_price.json", 'w', encoding='utf-8')
    # f.write(jsondata)
    # f.close()

    return car_price_name, car_price_mami


# 返回车品牌价格的平均值
def car_average_price(total_mes):
    new_car_price = {}
    for i in total_mes:
        if "暂无报价" in i["价格"]:
            continue
        if i["品牌"] not in new_car_price.keys():
            a = [eval(i["价格"][:-2])]
            new_car_price[i["品牌"]] = a
        else:
            new_car_price[i["品牌"]].append(eval(i["价格"][:-2]))
    for i in new_car_price.keys():
        new_car_price[i] = round(sum(new_car_price[i])/len(new_car_price[i]), 2)

    print(list(new_car_price.keys()))
    print(list(new_car_price.values()))


#  用来生成所有的车款评论信息的json文件于total_command.json,以及单一车款对应的评论信息
def one_car_re(name):
    # src = "data/data.txt"
    # new_text = read(src)
    # re_text = {}
    # for i in new_text:
    #     if i[8] == "暂无口碑数据\n":
    #         continue
    #     re_text[i[1]] = eval(i[8].replace("\\n", ""))
    # jsondata = json.dumps(re_text, indent=4, separators=(',', ': '), ensure_ascii=False)
    # f = open("static/total_command.json", 'w', encoding='utf-8')
    # f.write(jsondata)
    # f.close()

    f = open("static/total_command.json", 'r', encoding='utf-8')
    jsondata = json.load(f)
    f.close()

    car_name = list(jsondata[name].keys())
    re_num = list(jsondata[name].values())
    new_re_data = json.dumps({"car_name": car_name, "re_num": re_num}, indent=4, separators=(',', ': '), ensure_ascii=False)
    f = open("static/command_data/" + name + ".json", 'w', encoding='utf-8')
    f.write(new_re_data)
    f.close()


def main():
    src = "data/data.txt"
    new_text = read(src)  # 读取文本返回列表
    rand_num, total_mes = gra_one(new_text)  # 返回第一个车系数量分布图需要的数据
    car_average_price(total_mes)
    # car_price_name, car_price_mami = car_price(total_mes)  # 返回同一车系下不同车款的价格曲线
    # one_car_re(src)
    # power_total = power_type(total_mes)  # 返回车动力方式数量数据
    # car_name, car_sc = car_score(total_mes)  # 返回车系对应的评分
    # command, number = command_mes(new_text)  # 返回用户评论数量饼图所需的数据
    #  返回品牌名列表以及品牌下车系数量列表
    # rand_name_, total_mes_ = part_rand_series(rand_num=rand_num, total_mes=total_mes)


if __name__ == '__main__':
    main()