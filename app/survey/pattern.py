def find_pattern(code):
    result = ''
    code = code.split()
    bmi = get_bmi(to_number(code[4]), to_number(code[3]))

    result += get_gym_comment(bmi, to_number(code[6]), to_number(code[7]))
    result += get_diet_comment(to_number(code[8]))
    result += get_stress_comment(to_number(code[9]))
    if len(code) > 10:
        result += get_special_comment(code[10])
    return result


def get_gym_comment(bmi, body1, body2):
    if bmi < 17:
        if body1 == 1:
            if body2 <= 2:
                return '하체 근육량을 키우셔야 하는 마른 스타일이십니다.\n'
            else:
                return '몸을 균형있게 발달시킬 수 있는 운동을 추천합니다.\n'
        elif body1 == 2:
            if body2 <= 2:
                return '상체 근육량을 키우셔야 하는 마른 스타일이십니다.\n'
            else:
                return '몸을 균형있게 발달시킬 수 있는 운동을 추천합니다.\n'
        else:
            if body2 <= 2:
                return '상하체 근육량을 골고루 키우셔야 하는 마른 스타일이십니다.\n'
            else:
                return '본격적인 체력증진을 위한 운동을 할 몸의 준비가 되어있는 분으로 보이네요^^\n'
    elif bmi < 28:
        if body1 == 1:
            if body2 <= 2:
                return '하체 근육량을 키우셔야 하는 평범한 체형의 스타일이십니다.\n'
            else:
                return '몸을 균형있게 발달시킬 수 있는 운동을 추천합니다.\n'
        elif body1 == 2:
            if body2 <= 2:
                return '상체 근육량을 키우셔야 하는 평범한 체형의 스타일이십니다\n'
            else:
                return '몸을 균형있게 발달시킬 수 있는 운동을 추천합니다.\n'
        else:
            if body2 <= 2:
                return '상하체 근육량을 골고루 키우셔야 하는 평범한 체형의 스타일이십니다.\n'
            else:
                return '본격적인 체력증진을 위한 운동을 할 몸의 준비가 되어있는 분으로 보이네요^^\n'
    else:
        if body1 == 1:
            if body2 <= 2:
                return '일단 사이클과 같이 무릎에 무리가 가지 않는 유산소 운동이 필요해보입니다.\n'
            else:
                return '유산소 운동이 꼭!꼭! 필요해 보이시네요.\n'
        elif body1 == 2:
            if body2 <= 2:
                return '일단 사이클과 같이 무릎에 무리가 가지 않는 유산소 운동이 필요해보입니다.\n'
            else:
                return '유산소 운동이 꼭!꼭! 필요해 보이시네요.\n'
        else:
            if body2 <= 2:
                return '일단 사이클과 같이 무릎에 무리가 가지 않는 유산소 운동이 필요해보입니다.\n'
            else:
                return '유산소 운동이 꼭!꼭! 필요해 보이시네요.\n'


def get_diet_comment(diet):
    if diet <= 2:
        return '식습관에 대한 컨설팅이 필요하신 것으로 판단됩니다.\n'
    else:
        return '식습관은 나쁘지 않은 것 같네요. 하지만, 정확한 평가 없이 자만은 금물입니다!\n'


def get_stress_comment(stress):
    if stress <= 2:
        return '마지막으로, 스트레스는 만병의 근원이라고 합니다. 운동하러가자와 함께 스트레스 조절 연습을 해볼까요?'
    else:
        return '평균보다 건강한 정신력을 가지신 것 같네요. 그럼 힘차게 운동해 볼가요?'


def get_special_comment(sick):
    return '\n단, 운동을 시작하기 전에 꼭!꼭! 운동하러가자에 현재 몸의 상태에 대해 상담을 하시길 권장합니다.'


def to_number(letter):
    if letter == 'A':
        return 1
    elif letter == 'B':
        return 2
    elif letter == 'C':
        return 3
    else:
        return 4


def get_bmi(weight, height):
    return weight / (height * height)