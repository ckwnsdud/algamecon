import pygame
import random

# 초기 설정
pygame.init()

# 화면 크기 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Stage 1')

# 색상 및 폰트
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 36)

# 플레이어 설정
player_width = 40
player_height = 100
player_x = 100
player_y = SCREEN_HEIGHT - player_height - 50
player_velocity = 5
jump_height = 100
jump_time = 0.5
slide_height = 25
player_lives = 3

# 장애물 설정
obstacle_width = 30
obstacle_height = 30
obstacle_velocity = 5
min_obstacle_gap = 1000  # 장애물 생성 후 최소 1초 대기
max_obstacle_gap = 3000  # 최대 3초 대기
last_obstacle_time = 0  # 마지막 장애물이 생성된 시간

# 게임 시간
stage_duration = 180000  # 3분(밀리초)
clock = pygame.time.Clock()

# 게임 변수
is_jumping = False
is_sliding = False
jump_start_time = 0
slide_timer = 0
obstacles = []
game_over = False
stage_clear = False
start_time = pygame.time.get_ticks()

# 장애물 생성
def spawn_obstacle():
    obstacle_x = SCREEN_WIDTH
    
    # 장애물이 위쪽 또는 아래쪽에 나오게 설정
    if random.choice([True, False]):  # 랜덤으로 위쪽/아래쪽 설정
        obstacle_height = 30
        obstacle_y = SCREEN_HEIGHT - obstacle_height - 50  # 아래쪽
    else:
        obstacle_height = 430
        obstacle_y = 50  # 위쪽

    obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))


# 장애물 충돌 처리
def check_collision(player_rect, obstacles):
    for obstacle in obstacles:
        if player_rect.colliderect(obstacle):
            return True
    return False

# 플레이어 움직임
def move_player(keys_pressed, player_rect):
    global is_jumping, is_sliding, jump_start_time

    # 점프 동작
    if not is_jumping and not is_sliding:
        if keys_pressed[pygame.K_j]:  # 점프
            is_jumping = True
            jump_start_time = pygame.time.get_ticks()

    # 점프 처리
    if is_jumping:
        time_elapsed = (pygame.time.get_ticks() - jump_start_time) / 1000  # 초 단위 경과 시간
        if time_elapsed < jump_time / 2:
            player_rect.y = player_y - (jump_height * (2 * time_elapsed / jump_time))  # 점프 상승
        elif time_elapsed < jump_time:
            player_rect.y = player_y - (jump_height * (2 - 2 * time_elapsed / jump_time))  # 점프 하강
        else:
            player_rect.y = player_y
            is_jumping = False

    # 슬라이딩 처리
    if not is_jumping:  # 점프 중일 때는 슬라이드 불가
        if keys_pressed[pygame.K_k]:  # 슬라이드 키가 눌려있으면 슬라이딩
            is_sliding = True
        else:  # 슬라이드 키에서 손을 떼면 원래 높이로 복구
            is_sliding = False

    # 슬라이딩 중일 때 캐릭터 높이를 줄이고 아래쪽 부분만 남도록 y 좌표 조정
    if is_sliding:
        player_rect.height = slide_height
        player_rect.y = player_y + (player_height - slide_height)  # 캐릭터를 아래로 이동
    else:
        player_rect.height = player_height
        if not is_jumping:  # 점프 중이 아닐 때만 원래 위치로 복귀
            player_rect.y = player_y



# 게임 루프
while not game_over and not stage_clear:
    screen.fill(WHITE)
    elapsed_time = pygame.time.get_ticks() - start_time

    # 스테이지 클리어 체크
    if elapsed_time >= stage_duration:
        stage_clear = True

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # 키 입력
    keys_pressed = pygame.key.get_pressed()

    # 플레이어 이동
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    move_player(keys_pressed, player_rect)

    # 장애물 이동 및 생성
    current_time = pygame.time.get_ticks()
    if current_time - last_obstacle_time >= min_obstacle_gap:
        spawn_obstacle()
        last_obstacle_time = current_time  # 마지막 장애물 생성 시간 갱신

    for obstacle in obstacles:
        obstacle.x -= obstacle_velocity
        pygame.draw.rect(screen, RED, obstacle)

    # 충돌 체크
    if check_collision(player_rect, obstacles):
        player_lives -= 1
        obstacles.clear()  # 충돌 시 장애물 초기화
        if player_lives <= 0:
            game_over = True

    # 플레이어 및 UI 표시
    pygame.draw.rect(screen, RED, player_rect)
    lives_text = FONT.render(f"Lives: {player_lives}", True, RED)
    screen.blit(lives_text, (10, 10))

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 게임 종료 처리
if game_over:
    print("Game Over!")
elif stage_clear:
    print("Stage Cleared!")
