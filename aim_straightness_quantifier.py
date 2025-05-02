import math
import numpy


class HitObject:
        x: int
        y: int
        time: int
        type: int

class Input:
        x: float
        y: float
        time: int


def _intersect_point_circle(
                point_x: int,
                point_y: int,
                circle_x: int,
                circle_y: int,
                circle_radius: float
) -> bool:
        return math.sqrt(
                abs((point_x - circle_x) ** 2) +
                abs((point_y - circle_y) ** 2)
        ) <= circle_radius


def quantify_aim_straightness(
                hit_objects: list[HitObject], circle_size: float, inputs: list[Input]
) -> float:
        # Return max aim straightness if only one HitObject or Input
        if len(hit_objects) < 2 or len(inputs) < 2:
                return 1.0

        aim_straightness: list[float] = list(float)

        circle_radius: float = 54.4 - 4.48 * circle_size

        next_hit_object_index: int = 1
        for i in range(len(inputs)):
                # Don't quantify before first HitObject
                if inputs[i].time < hit_objects[0].time:
                        continue

                # Stop quantifying after last HitObject
                if inputs[i].time > hit_objects[-1].time:
                        break

                # Advance to next HitObject pair if time of inputs exceeds that of current one
                while hit_objects[next_hit_object_index].time < inputs[i].time:
                        next_hit_object_index += 1
                
                # Don't quantify if not hitcircle or slider
                if not hit_objects[next_hit_object_index].type & 0b00000011:
                        continue
                
                # Don't quantify if cursor is within HitObject
                if _intersect_point_circle(
                        inputs[i].x,
                        inputs[i].y,
                        hit_objects[next_hit_object_index].x,
                        hit_objects[next_hit_object_index].y,
                        circle_radius
                ):
                        continue

                """
                Calculate aim straightness based on dot product
                between aiming direction
                (abs(current_cursor_pos - previous_cursor_pos))
                and direction from previous to next hit object
                (abs(next_hit_object_pos - previous_hit_object_pos))
                """
                aim_straightness.append(
                        numpy.dot(
                                numpy.linalg.norm(
                                        numpy.array(
                                                inputs[i].x,
                                                inputs[i].y
                                        ) -
                                        numpy.array(
                                                inputs[i-1].x,
                                                inputs[i-1].y
                                        )
                                ),
                                numpy.linalg.norm(
                                        numpy.array(
                                                hit_objects[next_hit_object_index].x,
                                                hit_objects[next_hit_object_index].y
                                        ) -
                                        numpy.array(
                                                hit_objects[next_hit_object_index-1].x,
                                                hit_objects[next_hit_object_index-1].y
                                        )
                                )
                        )
                )
        
        # Return average of aim straightness quantifications
        return sum(aim_straightness) / len(aim_straightness)
