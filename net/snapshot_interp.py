"""第 52 批：联机对枪时敌人瞬移、回滚、子弹穿墙：快照插值用到..."""


def tick_alpha(render_tick, prev_tick, next_tick):
    """按服务器 tick 返回插值系数，钳制到 [0, 1]。"""
    span = next_tick - prev_tick
    if span <= 0:
        return 1.0
    alpha = (render_tick - prev_tick) / span
    return max(0.0, min(1.0, alpha))


def clamp_extrapolation(delta, max_delta):
    """限制快照外推距离，钳制到 [-max_delta, max_delta]。"""
    return max(-max_delta, min(max_delta, delta))


def pose_sync(position, rotation):
    """返回同步后的位姿：位置与旋转作为同一快照的原子对。"""
    return (position, rotation)


def rollback_world(players, doors):
    """返回包含玩家与门的回滚状态（全场景回滚，不只玩家）。"""
    return (players, doors)


def sequence_ok(seq, last_seq):
    """判断快照序号是否按序到达：只接受比最近序号更新的快照。"""
    return seq > last_seq


def clock_offset(local_time, remote_time):
    """返回本地与服务器时钟偏移（本地 - 远端）。"""
    return local_time - remote_time


def blend_prediction(authority, predicted, alpha):
    """在权威状态与预测状态之间插值，alpha=0 取权威，alpha=1 取预测。"""
    return authority + (predicted - authority) * alpha


def hit_at_rewind(current_pos, rewind_pos):
    """返回命中检测使用的回滚位置（用回滚位置而非当前位置）。"""
    return rewind_pos
