import requests
import os

# 开发者 API 密钥，从环境变量获取
API_KEY = os.getenv("LX_API")
BASE_URL = "https://maimai.lxns.net/api/v0"
USER_ID = os.getenv("CHUNI_USER_ID")  # 替换为实际的好友码

# 中二节奏枚举类型映射
CHUNITHM_LEVEL_INDEX_MAP = {
    0: "BASIC",
    1: "ADVANCED",
    2: "EXPERT",
    3: "MASTER",
    4: "ULTIMA"
}

CHUNITHM_RANK_MAP = {
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

CHUNITHM_CLEAR_MAP = {
    "clear": "CLEAR",
    "failed": "FAILED",
    "hard": "HARD",
    "brave": "BRAVE",
    "absolute": "ABSOLUTE",
    "catastrophy": "CATASTROPHY",
    "fullcombo": "FULL COMBO",
    "fullchain": "FULL CHAIN",
    "alljustice": "ALL JUSTICE"
}

CHUNITHM_FC_MAP = {
    "fc": "FC",
    "fcp": "FC+",
    "aj": "AJ",
    "ajc": "AJ+"
}

def chunithm_map_level_index(level_index):
    """转换中二节奏难度索引为文字"""
    return CHUNITHM_LEVEL_INDEX_MAP.get(level_index, str(level_index))

def chunithm_map_rank(rank):
    """转换中二节奏评级类型"""
    return CHUNITHM_RANK_MAP.get(rank, str(rank))

def chunithm_map_clear(clear):
    """转换中二节奏通关类型"""
    return CHUNITHM_CLEAR_MAP.get(clear, clear) if clear else None

def chunithm_map_fc(fc):
    """转换中二节奏FC类型"""
    return CHUNITHM_FC_MAP.get(fc, fc) if fc else None

def get_chunithm_player_info(friend_code):
    """获取中二节奏玩家基本信息"""
    headers = {"Authorization": API_KEY}
    
    try:
        resp = requests.get(
            f"{BASE_URL}/chunithm/player/{friend_code}", 
            headers=headers, 
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        
        if not data.get("success") or data.get("code") != 200:
            return None, f"中二节奏API错误：{data.get('message', '未知错误')}"
        
        return data["data"], None
    except Exception as e:
        return None, f"中二节奏获取失败：{str(e)}"

def get_chunithm_bests(friend_code):
    """获取中二节奏玩家Best数据"""
    headers = {"Authorization": API_KEY}
    
    try:
        resp = requests.get(
            f"{BASE_URL}/chunithm/player/{friend_code}/bests", 
            headers=headers, 
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        
        if not data.get("success") or data.get("code") != 200:
            return None, f"Best API错误：{data.get('message', '未知错误')}"
        
        return data["data"], None
    except Exception as e:
        return None, f"Best获取失败：{str(e)}"

def format_chunithm_score(score):
    """格式化中二节奏单个谱面成绩信息"""
    clear_type = chunithm_map_clear(score.get('clear'))
    fc_type = chunithm_map_fc(score.get('full_combo'))
    full_chain_type = score.get('full_chain')
    
    clear_display = f"  {clear_type}" if clear_type else ""
    fc_display = f" {fc_type}" if fc_type else ""
    chain_display = f"  {full_chain_type}" if full_chain_type else ""
    
    return (
        f"  曲名: {score.get('song_name', '未知')}\n"
        f"  难度: {score.get('level', '未知')} ({chunithm_map_level_index(score.get('level_index', ''))})\n"
        f"  分数: {score.get('score', 0)}  评级: {chunithm_map_rank(score.get('rank', '未知'))}\n"
        f"  Rating: {score.get('rating', 0):.4f}\n"
        f"\t{clear_display}\t{fc_display}\t{chain_display}\n"
    )

def get_full_chunithm_data(friend_code):
    """获取中二节奏玩家完整数据（基本信息+Best）"""
    # 获取基本信息
    player_data, player_error = get_chunithm_player_info(friend_code)
    if player_error:
        return None, player_error
    
    # 获取Best数据
    bests_data, bests_error = get_chunithm_bests(friend_code)
    if bests_error:
        return None, bests_error
    
    # 合并数据
    full_data = {
        "player_info": player_data,
        "bests": bests_data
    }
    
    return full_data, None

# 测试调用 + 写入文件（修复版）
if __name__ == "__main__":
    try:
        # 定义存储输出内容的字符串
        output_content = ""
        
        full_data, error = get_full_chunithm_data(USER_ID)
        
        if error:
            output_content = f"获取数据失败：{error}"
            print(output_content)
        else:
            player_info = full_data["player_info"]
            bests = full_data["bests"]
            
            # 拼接所有输出内容
            output_content += "=" * 60 + "\n"
            output_content += "中二节奏玩家基本信息".center(60) + "\n"
            output_content += "=" * 60 + "\n"
            output_content += f"玩家名称：{player_info.get('name')}\n"
            output_content += f"等级：{player_info.get('level')}\n"
            output_content += f"Rating：{player_info.get('rating')}\n"
            output_content += f"Overpower：{player_info.get('over_power')}\n"
            
            # 获取各部分数据
            bests_list = bests.get('bests', [])
            selections = bests.get('selections', [])
            new_bests = bests.get('new_bests', [])
            
            # 展示 Best 30
            if bests_list:
                output_content += "\n" + "=" * 60 + "\n"
                output_content += f"Best {len(bests_list)}".center(60) + "\n"
                output_content += "=" * 60 + "\n"
                for i, score in enumerate(bests_list, 1):
                    output_content += f"\n[{i}]\n"
                    output_content += format_chunithm_score(score)
            
            # 展示 New Best
            if new_bests:
                output_content += "\n" + "=" * 60 + "\n"
                output_content += f"New Best {len(new_bests)}".center(60) + "\n"
                output_content += "=" * 60 + "\n"
                for i, score in enumerate(new_bests, 1):
                    output_content += f"\n[{i}]\n"
                    output_content += format_chunithm_score(score)
        
        # 打印到控制台（方便调试）
        print(output_content)
        
        # 写入文件（用正确的字符串变量）
        with open("../../public/chunithm.txt", "w", encoding="utf-8") as f:
            f.write(output_content)

    except Exception as e:
        error_msg = f"程序错误：{e}"
        print(error_msg)
        # 错误也写入文件
        with open("../../public/chunithm.txt", "w", encoding="utf-8") as f:
            f.write(error_msg)
        import traceback
        traceback.print_exc()
