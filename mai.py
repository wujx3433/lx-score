import requests
import os

# 开发者 API 密钥，从环境变量获取
API_KEY = os.getenv("LX_API")
BASE_URL = "https://maimai.lxns.net/api/v0"
USER_ID = os.getenv("MAI_USER_ID")  # 替换为实际的好友码

# 枚举类型映射
LEVEL_INDEX_MAP = {
    0: "BASIC",
    1: "ADVANCED",
    2: "EXPERT",
    3: "MASTER",
    4: "Re:MASTER"
}

RATE_MAP = {
    "d": "D",
    "c": "C",
    "b": "B",
    "bb": "BB",
    "bbb": "BBB",
    "a": "A",
    "aa": "AA",
    "aaa": "AAA",
    "s": "S",
    "sp": "S+",
    "ss": "SS",
    "ssp": "SS+",
    "sss": "SSS",
    "sssp": "SSS+"
}

FC_MAP = {
    "fc": "FC",
    "fcp": "FC+",
    "ap": "AP",
    "app": "AP+"
}

FS_MAP = {
    "fs": "FS",
    "fsp": "FS+",
    "sync": "SYNC PLAY",
    "fsd": "FSD",
    "fsdp": "FSD+"
}

SONG_MAP = {
    "standard": "标准乐谱",
    "dx": "DX乐谱"
}

def map_level_index(level_index):
    """转换难度索引为文字"""
    return LEVEL_INDEX_MAP.get(level_index, str(level_index))

def map_rate(rate):
    """转换评级类型"""
    return RATE_MAP.get(rate, str(rate))

def map_fc(fc):
    """转换FC类型"""
    return FC_MAP.get(fc, fc) if fc else None

def map_fs(fs):
    """转换FS类型"""
    return FS_MAP.get(fs, fs) if fs else None

def map_song(song_type):    
    """转换谱面类型"""
    return SONG_MAP.get(song_type, song_type)


def get_maimai_player_info(friend_code):
    """获取舞萌玩家基本信息"""
    headers = {"Authorization": API_KEY}
    
    try:
        resp = requests.get(
            f"{BASE_URL}/maimai/player/{friend_code}", 
            headers=headers, 
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        
        if not data.get("success") or data.get("code") != 200:
            return None, f"舞萌API错误：{data.get('message', '未知错误')}"
        
        return data["data"], None
    except Exception as e:
        return None, f"舞萌获取失败：{str(e)}"

def get_maimai_bests(friend_code):
    """获取舞萌玩家B50数据"""
    headers = {"Authorization": API_KEY}
    
    try:
        resp = requests.get(
            f"{BASE_URL}/maimai/player/{friend_code}/bests", 
            headers=headers, 
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        
        if not data.get("success") or data.get("code") != 200:
            return None, f"B50 API错误：{data.get('message', '未知错误')}"
        
        return data["data"], None
    except Exception as e:
        return None, f"B50获取失败：{str(e)}"

def format_score(score):
    """格式化单个谱面成绩信息"""
    fc_type = map_fc(score.get('fc'))
    fs_type = map_fs(score.get('fs'))
    fc_display = f"  {fc_type}" if fc_type else ""
    fs_display = f"  {fs_type}" if fs_type else ""
    song_display = f"  谱面: {map_song(score.get('type', '未知'))}"
    
    return (
        f"  曲名: {score.get('song_name', '未知')}\n"
        f"  难度: {score.get('level', '未知')} ({map_level_index(score.get('level_index', ''))})\n"
        f"  达成率: {score.get('achievements', 0):.4f}%\n"
        f"  DX Rating: {int(score.get('dx_rating', 0))}  评级: {map_rate(score.get('rate', '未知'))}\n"
        f"\t{fc_display}\t{fs_display}\n"
    )

def get_full_maimai_data(friend_code):
    """获取舞萌玩家完整数据（基本信息+B50）"""
    # 获取基本信息
    player_data, player_error = get_maimai_player_info(friend_code)
    if player_error:
        return None, player_error
    
    # 获取B50数据
    bests_data, bests_error = get_maimai_bests(friend_code)
    if bests_error:
        return None, bests_error
    
    # 合并数据
    full_data = {
        "player_info": player_data,
        "bests": bests_data
    }
    
    return full_data, None

if __name__ == "__main__":
    try:
        # 定义输出字符串变量，存储所有内容
        output_content = ""
        
        full_data, error = get_full_maimai_data(USER_ID)
        
        if error:
            output_content = f"获取数据失败：{error}"
            print(output_content)
        else:
            player_info = full_data["player_info"]
            bests = full_data["bests"]
            
            # 拼接所有文本
            output_content += "=" * 60 + "\n"
            output_content += "舞萌玩家基本信息".center(60) + "\n"
            output_content += "=" * 60 + "\n"
            output_content += f"玩家名称：{player_info.get('name')}\n"
            output_content += f"Rating：{player_info.get('rating')}\n"
            
            output_content += "\n" + "=" * 60 + "\n"
            output_content += "B50 数据汇总".center(60) + "\n"
            output_content += "=" * 60 + "\n"
            output_content += f"旧版本 Best 35 总分：{bests.get('standard_total')}\n"
            output_content += f"现版本 Best 15 总分：{bests.get('dx_total')}\n"
            
            # 获取数据
            standard_scores = bests.get('standard', [])
            dx_scores = bests.get('dx', [])
            
            # 先展示旧版本 Best 35（完整）
            if standard_scores:
                output_content += "\n" + "=" * 60 + "\n"
                output_content += f"旧版本 Best {len(standard_scores)}".center(60) + "\n"
                output_content += "=" * 60 + "\n"
                for i, score in enumerate(standard_scores, 1):
                    output_content += f"\n[{i}]\n"
                    output_content += format_score(score)
            
            # 再展示现版本 Best 15（完整）
            if dx_scores:
                output_content += "\n" + "=" * 60 + "\n"
                output_content += f"现版本 Best {len(dx_scores)}".center(60) + "\n"
                output_content += "=" * 60 + "\n"
                for i, score in enumerate(dx_scores, 1):
                    output_content += f"\n[{i}]\n"
                    output_content += format_score(score)
        
        # 打印到控制台
        print(output_content)
        
        # 写入文件（使用正确的字符串变量）
        with open("../../public/maimai.txt", "w", encoding="utf-8") as f:
            f.write(output_content)

    except Exception as e:
        error_msg = f"程序错误：{e}"
        print(error_msg)
        # 错误信息写入文件
        with open("../../public/maimai.txt", "w", encoding="utf-8") as f:
            f.write(error_msg)
        import traceback
        traceback.print_exc()
