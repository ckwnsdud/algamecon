import pygame, sys, random
from pygame.locals import *

# 사운드 설정
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 512)

# 메인 게임 함수
def main():
    # 게임 초기화 정보
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Stage 1')

    # 게임오버 이미지 로드
    game_over_image = pygame.image.load('game_over.png')
    game_over_image = pygame.transform.scale(game_over_image, (screen_width, screen_height))

    # 배경 이미지 31장 로드 및 리스트 저장
    background_images = []
    for i in range(1, 32): 
        image = pygame.image.load(f'stage1_backgroun_{i}.png')
        image = pygame.transform.scale(image, (screen_width, screen_height))
        background_images.append(image)

    # 배경 이미지 인덱스 및 타이머 설정
    background_index = 0
    background_change_time = 600  # 배경 이미지 변경 간격 (밀리초)
    last_background_change = pygame.time.get_ticks()

    # 목숨 이미지
    heart_full_image = pygame.image.load('heart_full.png')
    heart_full_image = pygame.transform.scale(heart_full_image, (40, 40))

    heart_half_image = pygame.image.load('heart_half.png')
    heart_half_image = pygame.transform.scale(heart_half_image, (40, 40))
    
    heart_empty_image = pygame.image.load('heart_empty.png')
    heart_empty_image = pygame.transform.scale(heart_empty_image, (40, 40))


    # 플레이어 달리기 이미지 6장 로드 및 리스트 저장
    player_running_images = []
    for i in range(1, 7):  
        image = pygame.image.load(f'run{i}.png')
        image = pygame.transform.scale(image, (75, 100))
        player_running_images.append(image)

    # 플레이어 점프 이미지 6장 로드
    player_jumping_images = []
    for i in range(1, 7):
        image = pygame.image.load(f'jump{i}.png')
        image = pygame.transform.scale(image, (75, 100))
        player_jumping_images.append(image)

    # 플레이어 슬라이딩 이미지 4장 로드
    player_sliding_images = []
    for i in range(1, 5):
        image = pygame.image.load(f'sliding{i}.png')
        image = pygame.transform.scale(image, (100, 80))
        player_sliding_images.append(image)
    
    # 플레이어 객체 생성
    player = pygame.Rect((screen_width-75)/4, (screen_height-100)*3/4, 75, 100)

    # 플레이어 이미지 인덱스 및 타이머 설정
    running_image_index = 0
    jumping_image_index = 0
    sliding_image_index = 0
    last_player_image_change = pygame.time.get_ticks()

    # 목숨 변수
    heart = 3

    # 장애물 변수
    obstacle_velocity = 5
    min_obstacle_gap = 300  # 장애물 생성 후 최소 0.3초 대기
    max_obstacle_gap = 1000  # 최대 1초 대기
    last_obstacle_time = 0  # 마지막 장애물이 생성된 시간

    obstacle1_image = pygame.image.load('obstacle1.png')
    obstacle1_image = pygame.transform.scale(obstacle1_image, (90, 400))

    obstacle2_image = pygame.image.load('obstacle2.png')
    obstacle2_image = pygame.transform.scale(obstacle2_image, (40, 40))

    # 장애물 리스트
    obstacles = []

    # 게임 속도 조절
    clock = pygame.time.Clock()
    game_speed = 0.5

    # 중력
    y_vel = 0

    # 슬라이딩 여부 변수
    is_sliding = False
    is_jumping = False

    # 사운드 음악 설정
    jump_sound = pygame.mixer.Sound('jump_sound.wav')
    jump_sound.set_volume(0.3)
    sliding_sound = pygame.mixer.Sound('sliding_sound.wav')
    sliding_sound.set_volume(0.3)

    # 타이머 시작 시간 기록
    start_time = pygame.time.get_ticks()

    # 게임 
    while True:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # 게임 종료 시 게임오버 화면 띄우기
        if heart <= 0:
            screen.blit(game_over_image, (0, 0))
            pygame.display.update()
            pygame.time.delay(3000)  # 3초간 대기
            pygame.quit()
            sys.exit()

        current_time = pygame.time.get_ticks()
        
        # 1분 타이머 체크 (60,000 밀리초 = 60초)
        if current_time - start_time >= 60000:
            print("Game Over! Time's up!")
            pygame.quit()
            sys.exit()

        # 배경 이미지 변경
        if current_time - last_background_change >= background_change_time:
            background_index = (background_index + 1) % 31  # 0부터 30까지 순환
            last_background_change = current_time

        # 플레이어 달리기 애니메이션
        if not is_jumping and not is_sliding:
            if current_time - last_player_image_change >= (background_change_time - 400):  # 배경 변경 속도와 맞춤
                running_image_index = (running_image_index + 1) % len(player_running_images)
                last_player_image_change = current_time

        # 키 입력 정의
        keyInput = pygame.key.get_pressed()

        # 좌우 이동
        if keyInput[K_a] and player.left >= 0:
            player.left -= game_speed * dt
        if keyInput[K_d] and player.right <= screen_width:
            player.right += game_speed * dt

        # 중력 엔진 만들기
        if not is_sliding:
            player.top += y_vel
            y_vel += 1

        # 점프
        if player.bottom >= (screen_height-100)*14/15 and not is_sliding:
            y_vel = 0
            if keyInput[K_j] and not is_jumping:
                is_jumping = True
                jump_sound.play()
                jumping_image_index = 0
                y_vel = -18

        if is_jumping:
            if current_time - last_player_image_change >= 100:
                jumping_image_index = (jumping_image_index + 1) % len(player_jumping_images)
                last_player_image_change = current_time

            if player.bottom >= (screen_height-100)*14/15:
                is_jumping = False

        # 슬라이딩
        if keyInput[K_k] and not is_jumping and not is_sliding:
            sliding_sound.play()
            is_sliding = True
            sliding_image_index = 0
            player.height = 40
            player.top = (screen_height-100)*14/15 - 60
            
        elif not keyInput[K_k] and is_sliding:
            is_sliding = False
            player.height = 100
            player.top = (screen_height-100)*14/15 - 100
            
        if is_sliding:
            if current_time - last_player_image_change >= 200:  
                sliding_image_index = (sliding_image_index + 1) % len(player_sliding_images)
                last_player_image_change = current_time

        # 충돌 체크
        for obstacle, obstacle_image in obstacles:  
            if player.colliderect(obstacle):  
                obstacles.remove((obstacle, obstacle_image))  # 해당 장애물만 리스트에서 제거
                heart -= 1


        # 배경 그리기
        screen.blit(background_images[background_index], (0, 0))

        # 플레이어 그리기 (달리기, 점프, 슬라이딩 이미지)
        if is_jumping:
            screen.blit(player_jumping_images[jumping_image_index], player)
        elif is_sliding:
            screen.blit(player_sliding_images[sliding_image_index], player)
        else:
            screen.blit(player_running_images[running_image_index], player)
        
        # 목숨 그리기
        if heart == 3:
            screen.blit(heart_full_image, (80, 0))
            screen.blit(heart_half_image, (40, 0))
            screen.blit(heart_empty_image, (0, 0))
        elif heart == 2:
            screen.blit(heart_half_image, (40, 0))
            screen.blit(heart_empty_image, (0, 0))
        elif heart == 1:
            screen.blit(heart_empty_image, (0, 0))

        # 장애물 이동 및 생성
        current_time = pygame.time.get_ticks()

        if current_time - last_obstacle_time >= min_obstacle_gap:
            if random.choice([True, False]):
                # 장애물 1 생성 (높은 장애물)
                obstacle = pygame.Rect(screen_width, screen_height - 600, 90, 400)
                obstacles.append((obstacle, obstacle1_image))
            else:
                # 장애물 2 생성 (낮은 장애물)
                obstacle = pygame.Rect(screen_width, (screen_height-100)*7/8, 40, 40)
                obstacles.append((obstacle, obstacle2_image))
            last_obstacle_time = current_time + random.randint(min_obstacle_gap, max_obstacle_gap)  # 다음 생성 시간 랜덤

        # 장애물 이동 및 화면에 그리기
        for obstacle, obstacle_image in obstacles[:]:
            obstacle.x -= obstacle_velocity  # 왼쪽으로 이동
            screen.blit(obstacle_image, obstacle)

            # 장애물이 화면 밖으로 나가면 리스트에서 제거
            if obstacle.right < 0:
                obstacles.remove((obstacle, obstacle_image))

        pygame.display.update()

main()
