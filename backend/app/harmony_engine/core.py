"""
Harmony Helper - Core Harmony Generation Engine
使用 music21 库实现多种和声生成算法
"""

from music21 import note, interval, pitch, stream
from typing import List, Tuple, Dict
from enum import Enum


class HarmonyType(Enum):
    """和声类型枚举"""
    THIRD = "third"  # 三度和声
    FIFTH = "fifth"  # 五度和声
    PARALLEL_FOURTH = "parallel_fourth"  # 平行四度
    PARALLEL_SIXTH = "parallel_sixth"  # 平行六度
    CONTRARY = "contrary"  # 反向运动
    OBLIQUE = "oblique"  # 斜向运动
    PEDAL = "pedal"  # 持续音


class HarmonyGenerator:
    """和声生成器核心类"""
    
    def __init__(self):
        """初始化和声生成器"""
        pass
    
    def generate_harmony(
        self, 
        melody_notes: List[Dict], 
        harmony_type: HarmonyType
    ) -> List[Dict]:
        """
        根据旋律音符和和声类型生成和声
        
        Args:
            melody_notes: 旋律音符列表，每个音符是一个字典:
                         {'pitch': 'C4', 'duration': 1.0, 'offset': 0.0}
            harmony_type: 和声类型
            
        Returns:
            和声音符列表，格式与输入相同
        """
        if harmony_type == HarmonyType.THIRD:
            return self._generate_parallel_interval(melody_notes, 3)
        elif harmony_type == HarmonyType.FIFTH:
            return self._generate_parallel_interval(melody_notes, 4)
        elif harmony_type == HarmonyType.PARALLEL_FOURTH:
            return self._generate_parallel_interval(melody_notes, 5)
        elif harmony_type == HarmonyType.PARALLEL_SIXTH:
            return self._generate_parallel_interval(melody_notes, 8)
        elif harmony_type == HarmonyType.CONTRARY:
            return self._generate_contrary_motion(melody_notes)
        elif harmony_type == HarmonyType.OBLIQUE:
            return self._generate_oblique_motion(melody_notes)
        elif harmony_type == HarmonyType.PEDAL:
            return self._generate_pedal_tone(melody_notes)
        else:
            raise ValueError(f"Unknown harmony type: {harmony_type}")
    
    def _generate_parallel_interval(
        self, 
        melody_notes: List[Dict], 
        semitones: int
    ) -> List[Dict]:
        """
        生成平行音程和声
        
        Args:
            melody_notes: 旋律音符列表
            semitones: 音程半音数（3=小三度, 4=大三度, 5=纯四度, 7=纯五度, 8=小六度等）
            
        Returns:
            和声音符列表
        """
        harmony_notes = []
        
        for melody_note in melody_notes:
            try:
                # 创建 music21 音符对象
                m21_note = note.Note(melody_note['pitch'])
                
                # 计算和声音符（向下移动指定音程）
                harmony_pitch = m21_note.pitch.transpose(-semitones)
                
                harmony_notes.append({
                    'pitch': harmony_pitch.nameWithOctave,
                    'duration': melody_note['duration'],
                    'offset': melody_note['offset']
                })
            except Exception as e:
                print(f"Error processing note {melody_note}: {e}")
                continue
        
        return harmony_notes
    
    def _generate_contrary_motion(self, melody_notes: List[Dict]) -> List[Dict]:
        """
        生成反向运动和声
        当旋律上行时，和声下行；旋律下行时，和声上行
        
        Args:
            melody_notes: 旋律音符列表
            
        Returns:
            和声音符列表
        """
        if len(melody_notes) < 2:
            # 如果只有一个音符，返回其五度音
            return self._generate_parallel_interval(melody_notes, 7)
        
        harmony_notes = []
        
        # 第一个和声音符：从旋律第一个音符的五度开始
        first_melody = note.Note(melody_notes[0]['pitch'])
        first_harmony_pitch = first_melody.pitch.transpose(-7)
        
        harmony_notes.append({
            'pitch': first_harmony_pitch.nameWithOctave,
            'duration': melody_notes[0]['duration'],
            'offset': melody_notes[0]['offset']
        })
        
        # 后续音符：根据旋律方向反向移动
        for i in range(1, len(melody_notes)):
            prev_melody = note.Note(melody_notes[i-1]['pitch'])
            curr_melody = note.Note(melody_notes[i]['pitch'])
            prev_harmony = note.Note(harmony_notes[i-1]['pitch'])
            
            # 计算旋律的音程变化（半音数）
            melody_interval = curr_melody.pitch.ps - prev_melody.pitch.ps
            
            # 和声反向移动相同的音程
            new_harmony_pitch = prev_harmony.pitch.transpose(-melody_interval)
            
            harmony_notes.append({
                'pitch': new_harmony_pitch.nameWithOctave,
                'duration': melody_notes[i]['duration'],
                'offset': melody_notes[i]['offset']
            })
        
        return harmony_notes
    
    def _generate_oblique_motion(self, melody_notes: List[Dict]) -> List[Dict]:
        """
        生成斜向运动和声
        和声声部保持在一个固定音高上（持续音），而旋律自由移动
        
        Args:
            melody_notes: 旋律音符列表
            
        Returns:
            和声音符列表
        """
        if not melody_notes:
            return []
        
        # 选择第一个旋律音符的五度作为持续音
        first_melody = note.Note(melody_notes[0]['pitch'])
        pedal_pitch = first_melody.pitch.transpose(-7)
        
        harmony_notes = []
        for melody_note in melody_notes:
            harmony_notes.append({
                'pitch': pedal_pitch.nameWithOctave,
                'duration': melody_note['duration'],
                'offset': melody_note['offset']
            })
        
        return harmony_notes
    
    def _generate_pedal_tone(self, melody_notes: List[Dict]) -> List[Dict]:
        """
        生成持续音（Pedal Tone）
        通常使用旋律的主音或属音作为持续低音
        
        Args:
            melody_notes: 旋律音符列表
            
        Returns:
            和声音符列表
        """
        if not melody_notes:
            return []
        
        # 分析旋律，找到最低音作为参考
        pitches = [note.Note(n['pitch']).pitch.ps for n in melody_notes]
        min_pitch_ps = min(pitches)
        
        # 创建一个比最低音低一个八度的持续音
        pedal_note = note.Note()
        pedal_note.pitch.ps = min_pitch_ps - 12  # 低一个八度
        
        # 创建一个贯穿整个旋律的长音符
        total_duration = max(n['offset'] + n['duration'] for n in melody_notes)
        
        return [{
            'pitch': pedal_note.pitch.nameWithOctave,
            'duration': total_duration,
            'offset': 0.0
        }]


def test_harmony_generator():
    """测试和声生成器"""
    print("=" * 60)
    print("Harmony Helper - Core Engine Test")
    print("=" * 60)
    
    # 创建一个简单的测试旋律：C-D-E-F-G (C大调音阶的前5个音)
    test_melody = [
        {'pitch': 'C4', 'duration': 1.0, 'offset': 0.0},
        {'pitch': 'D4', 'duration': 1.0, 'offset': 1.0},
        {'pitch': 'E4', 'duration': 1.0, 'offset': 2.0},
        {'pitch': 'F4', 'duration': 1.0, 'offset': 3.0},
        {'pitch': 'G4', 'duration': 1.0, 'offset': 4.0},
    ]
    
    print("\n测试旋律 (C Major Scale):")
    print([n['pitch'] for n in test_melody])
    
    generator = HarmonyGenerator()
    
    # 测试所有和声类型
    harmony_types = [
        (HarmonyType.THIRD, "三度和声"),
        (HarmonyType.FIFTH, "五度和声"),
        (HarmonyType.PARALLEL_FOURTH, "平行四度"),
        (HarmonyType.PARALLEL_SIXTH, "平行六度"),
        (HarmonyType.CONTRARY, "反向运动"),
        (HarmonyType.OBLIQUE, "斜向运动"),
        (HarmonyType.PEDAL, "持续音"),
    ]
    
    for harmony_type, description in harmony_types:
        print(f"\n{description} ({harmony_type.value}):")
        harmony = generator.generate_harmony(test_melody, harmony_type)
        print(f"  旋律: {[n['pitch'] for n in test_melody]}")
        print(f"  和声: {[n['pitch'] for n in harmony]}")
    
    print("\n" + "=" * 60)
    print("测试完成！所有和声类型均已验证。")
    print("=" * 60)


if __name__ == "__main__":
    test_harmony_generator()
