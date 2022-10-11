# drumDrum by Gesty Linaga 
import pygame, os
from pygame import mixer
pygame.init()

# App-wide settings:
WIDTH, HEIGHT = 1400, 800
WIN = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("drumDrum")
FONT = pygame.font.SysFont("consolas", 32)
BOLD_FONT = pygame.font.SysFont("consolas", 32, bold=pygame.font.Font.bold)
SMALL_FONT = pygame.font.SysFont("consolas", 24)

# Defining colors:
RED = (247, 118, 142) # not used
GREEN = (158, 206, 106)
BLUE = (122, 162, 247) # not used
YELLOW = (224, 175, 104)
ORANGE = (255, 158, 100) # not used
TEAL = (115, 218, 202)
MAGENTA = (187, 154, 247) # not used
BG = (36, 40, 59)
BLACK = (15, 15, 20)
WHITE = (213, 214, 219)
GRAY1 = (169, 177, 214)
GRAY2 = (154, 165, 206) # not used
GRAY3 = (86, 95, 137)
GRAY4 = (65, 72, 104)

# Game-wide settings/vars:
FPS = 60 # hardcoded fps cap
CLOCK = pygame.time.Clock()
BEATS = 8 # aka columns
INSTRUMENTS = 6 # aka rows
CLICKED = [[-1 for _ in range(BEATS)] for _ in range(INSTRUMENTS)] # 8x6 grid of '-1's (off state)
ACTIVE_LIST = [1 for _ in range(INSTRUMENTS)] # vertical line of '1's (on state)
BPM = 240 # beats per minute
PLAYING = True # default state
ACTIVE_BEAT = 0 # default starting beat
ACTIVE_LENGTH = 0 # length of current grid 
BEAT_CHANGED = True # check if num of beats changed
SAVE_MENU = False # save menu state
LOAD_MENU = False # load menu state

# Save data file:
SAVED_BEATS = [] 
FILE = open('./saved_beats.txt', 'r') # open file in read mode
# Loads saved beats locally:
for line in FILE: 
    SAVED_BEATS.append(line)
BEAT_NAME = '' # starting beat name
TYPING = False # typing state
INDEX = 100 # for choosing load file (100 keeps it out of sight)

# Import sounds:
RIDE = mixer.Sound(os.path.join('sounds', 'ride.wav'))
RIDE.set_volume(0.5) # lowering volume
HIHAT_OPEN = mixer.Sound(os.path.join('sounds', 'hihatOpen.wav'))
HIHAT_OPEN.set_volume(0.5) # lowering volume
HIHAT_CLOSED = mixer.Sound(os.path.join('sounds', 'hihatClosed.wav'))
HIHAT_CLOSED.set_volume(0.5) # lowering volume
SNARE = mixer.Sound(os.path.join('sounds', 'snare.wav'))
FLOOR_TOM = mixer.Sound(os.path.join('sounds', 'floorTom.wav'))
KICK = mixer.Sound(os.path.join('sounds', 'kick.wav'))
# Raises num of channels played at a time
mixer.set_num_channels(INSTRUMENTS * 10) # incase of too many boxes are clicked

# Playing sounds:
def playSounds():
    for i in range(len(CLICKED)): # iterate across grid
        # If clicked on, AND in active column:
        if CLICKED[i][ACTIVE_BEAT] == 1 and ACTIVE_LIST[i] == 1:
            if i == 0:
                RIDE.play()
            if i == 1:
                HIHAT_OPEN.play()
            if i == 2:
                HIHAT_CLOSED.play()
            if i == 3:
                SNARE.play()
            if i == 4:
                FLOOR_TOM.play()
            if i == 5:
                KICK.play()

# Drawing click grid:
def drawGrid(clicks, beat, actives):
    # Menu Boxes:
    leftBox = pygame.draw.rect(WIN, GRAY4, [0, 0, 220, HEIGHT - 200], 5)
    bottomBox = pygame.draw.rect(WIN, GRAY4, [0, HEIGHT - 200, WIDTH, 200], 5)

    boxes = [] # to hold click grid
    colors = [GRAY1, WHITE, GRAY1] # click grid states (on/off)

    # Instrument Labels:
    ride_text = FONT.render("Ride", True, colors[actives[0]])
    WIN.blit(ride_text, (10, 30))
    hihatOpen_text = FONT.render("HiHat Open", True, colors[actives[1]])
    WIN.blit(hihatOpen_text, (10, 130))
    hihatClosed_text = FONT.render("HiHatClosed", True, colors[actives[2]])
    WIN.blit(hihatClosed_text, (10, 230))
    snare_text = FONT.render("Snare", True, colors[actives[3]])
    WIN.blit(snare_text, (10, 330))
    floorTom_text = FONT.render("Floor Tom", True, colors[actives[4]])
    WIN.blit(floorTom_text, (10, 430))
    kick_text = FONT.render("Kick", True, colors[actives[5]])
    WIN.blit(kick_text, (10, 530))

    # Border between instrument names:
    for i in range(6):
        pygame.draw.line(WIN, GRAY4, (0, (i * 100) + 100), (215, (i * 100) + 100), 3)

    # Draw beats grid:
    for i in range(BEATS): # columns
        for j in range(INSTRUMENTS): # rows
            if clicks[j][i] == -1: # if clicked off
                color = GRAY3
            else:
                if actives[j] == 1: # clicked on
                    color = GREEN
                else: # active, but not clicked
                    color = GRAY1

            # Draw box grid:
            rect = pygame.draw.rect(WIN, color, [i * ((WIDTH - 220) // BEATS) + 225, (j * 100) + 5, ((WIDTH - 200) // BEATS) - 10, ((HEIGHT - 200) // INSTRUMENTS) - 10], 0, 3)

            # Grid decoration border:
            pygame.draw.rect(WIN, YELLOW, [i * ((WIDTH - 220) // BEATS) + 220, (j * 100), ((WIDTH - 200) // BEATS), ((HEIGHT - 200) // INSTRUMENTS)], 3, 3)
            pygame.draw.rect(WIN, BLACK, [i * ((WIDTH - 220) // BEATS) + 220, (j * 100), ((WIDTH - 200) // BEATS), ((HEIGHT - 200) // INSTRUMENTS)], 1, 3)

            # Add box to grid with (color, (x,y)):
            boxes.append((rect, (i, j)))

        # Active/Playing beat outline
        active = pygame.draw.rect(WIN, TEAL, [beat * ((WIDTH - 220) // BEATS) + 220, 0, ((WIDTH - 220) // BEATS), INSTRUMENTS * 100], 5, 3)

    return boxes # final grid

# Drawing save beats menu:
def drawSaveMenu(BEAT_NAME, TYPING):
    # Redraws bg over screen:
    pygame.draw.rect(WIN, BG, [0, 0, WIDTH, HEIGHT]) 

    # Menu label:
    menuText = BOLD_FONT.render('SAVE MENU: Enter a Name for Current Beat', True, WHITE)
    WIN.blit(menuText, (275, 40))

    # Save Buton:
    savingBtn = pygame.draw.rect(WIN, GRAY4, [WIDTH // 2 - 200, HEIGHT * 0.75, 400, 100], 0, 5)
    savingTxt = BOLD_FONT.render('Save Beat', True, WHITE)
    WIN.blit(savingTxt, (WIDTH // 2 - 90, HEIGHT * 0.75 + 40))

    # Exit Button:
    exitBtn = pygame.draw.rect(WIN, GRAY4, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exitTxt = BOLD_FONT.render('Close', True, WHITE)
    WIN.blit(exitTxt, (WIDTH - 160, HEIGHT - 70))

    # If clicked into typing area:
    if TYPING: 
        # Change text box color:
        pygame.draw.rect(WIN, GRAY4, [400, 200, 600, 200], 0, 5)

    # Entry box:
    entryRect = pygame.draw.rect(WIN, GRAY3, [400, 200, 600, 200], 5, 5)
    entryTxt = FONT.render(f'{BEAT_NAME}', True, WHITE)
    WIN.blit(entryTxt, (430, 250))

    return exitBtn, savingBtn, entryRect

# Drawing load beats menu:
def drawLoadMenu(INDEX):
    # Empty defaults:
    loadedClicked = []
    loadedBeats = 0 
    loadedBpm = 0 

    # Redraws bg over screen:
    pygame.draw.rect(WIN, BG, [0, 0, WIDTH, HEIGHT]) 

    # Menu label:
    menuText = BOLD_FONT.render('LOAD MENU: Select a Beat to Load', True, WHITE)
    WIN.blit(menuText, (400, 40))

    # Loading button:
    loadingBtn = pygame.draw.rect(WIN, GRAY4, [WIDTH //2 - 200, HEIGHT * 0.87, 400, 90], 0, 5)
    loadingTxt = BOLD_FONT.render('Load Beat', True, WHITE)
    WIN.blit(loadingTxt, (WIDTH // 2 - 90, HEIGHT * 0.87 + 30))

    # Delete button:
    deleteBtn = pygame.draw.rect(WIN, GRAY4, [(WIDTH//2) - 510, HEIGHT * 0.87, 200, 90], 0, 5)
    deleteTxt = BOLD_FONT.render('Delete', True, WHITE)
    WIN.blit(deleteTxt, ((WIDTH//2) - 475, HEIGHT * 0.87 + 30))

    # Exit button:
    exitBtn = pygame.draw.rect(WIN, GRAY4, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exitTxt = BOLD_FONT.render('Close', True, WHITE)
    WIN.blit(exitTxt, (WIDTH - 160, HEIGHT -70))

    # Loaded selection rectangle:
    loadedRectangle = pygame.draw.rect(WIN, GRAY4, [190, 90, 1000, 600], 5, 5)
    if 0 <= INDEX < len(SAVED_BEATS): # if clicked inside selection box
        pygame.draw.rect(WIN, GRAY4, [190, 90 + INDEX * 50, 1000, 55]) # change bg of selection

    # Loading choices from save file:
    for beat in range(len(SAVED_BEATS)):
        if beat < 10: # hardcap of number of saved beats
            beatClicked = [] # Empty to hold beat grid of save file

            # Beat label:
            rowText = SMALL_FONT.render(f'{beat + 1}', True, WHITE)
            WIN.blit(rowText, (200, 110 + beat * 50))

            # Indexing name from save file and displaying:
            nameIndexStart = SAVED_BEATS[beat].index('name: ') + 6 # start point for name in string
            nameIndexEnd = SAVED_BEATS[beat].index(', beats:') # end point for name in string
            nameText = SMALL_FONT.render(SAVED_BEATS[beat][nameIndexStart:nameIndexEnd], True, WHITE) # slicing name out of string
            WIN.blit(nameText, (240, 110 + beat * 50))

        # Indexing beat/bpm/grid info from save file:
        if 0 <= INDEX < len(SAVED_BEATS) and beat == INDEX: # if beat selected is valid/chosen:
            beatIndexEnd = SAVED_BEATS[beat].index(', bpm:')
            loadedBeats = int(SAVED_BEATS[beat][nameIndexEnd + 8:beatIndexEnd]) # slicing beats

            bpmIndexEnd = SAVED_BEATS[beat].index(', selected:')
            loadedBpm = int(SAVED_BEATS[beat][beatIndexEnd + 6: bpmIndexEnd]) # slicing bpm

            loadedClicksString = SAVED_BEATS[beat][bpmIndexEnd + 14: -3]
            loadedClicksRows = list(loadedClicksString.split('], [')) # slicing grid

            # Splitting grid string into a real grid:
            for row in range(len(loadedClicksRows)):
                loadedClicksRow = (loadedClicksRows[row].split(', ')) # splitting line into rows
                for item in range(len(loadedClicksRow)):
                    if loadedClicksRow[item] == '1' or loadedClicksRow[item] == '-1': # validates row items
                        loadedClicksRow[item] = int(loadedClicksRow[item]) # converts row string items into integers
                beatClicked.append(loadedClicksRow) # add row to temp grid
                loadedClicked = beatClicked # save completed grid to var

    # Returning loaded info into grid:
    loadedInfo = [loadedBeats, loadedBpm, loadedClicked] # saved beat choices to load
    return exitBtn, loadingBtn, deleteBtn, loadedRectangle, loadedInfo


# Main Game Loop:
run = True
while run:

    CLOCK.tick(FPS) # tick time
    WIN.fill(BG) # draw background

    # Create box grid:
    boxes = drawGrid(CLICKED, ACTIVE_BEAT, ACTIVE_LIST)

    # Lower Menu Box: #
    # Play/Pause
    playPause = pygame.draw.rect(WIN, GRAY4, [50, HEIGHT - 150, 200, 100], 0, 5) # border
    playText = SMALL_FONT.render('Play/Pause', True, WHITE) # label
    WIN.blit(playText, (70, HEIGHT - 130)) # draws to screen
    if PLAYING: # change text depending on state:
        playText2 = SMALL_FONT.render('Playing', True, BG)
    else:
        playText2 = SMALL_FONT.render('Paused', True, BG)
    WIN.blit(playText2, (70, HEIGHT - 100)) # draws to screen

    # BPM buttons
    bpmRect = pygame.draw.rect(WIN, GRAY4, [300, HEIGHT - 150, 225, 100], 5, 5)
    bpmText = SMALL_FONT.render('Beats Per Minute', True, WHITE)
    WIN.blit(bpmText, (308, HEIGHT - 130))
    bpmText2 = SMALL_FONT.render(f'{BPM}', True, WHITE)
    WIN.blit(bpmText2, (370, HEIGHT - 100))
    # +/- BPM buttons
    bpmAddRect = pygame.draw.rect(WIN, GRAY4, [530, HEIGHT - 150, 48, 48], 0, 5)
    addText = SMALL_FONT.render('+5', True, WHITE)
    WIN.blit(addText, (540, HEIGHT - 140))
    bpmSubRect = pygame.draw.rect(WIN, GRAY4, [530, HEIGHT - 100, 48, 48], 0, 5)
    subText = SMALL_FONT.render('-5', True, WHITE)
    WIN.blit(subText, (540, HEIGHT - 90))

    # Beats buttons
    beatsRect = pygame.draw.rect(WIN, GRAY4, [600, HEIGHT - 150, 200, 100], 5, 5)
    beatsText = SMALL_FONT.render('Beats in Loop', True, WHITE)
    WIN.blit(beatsText, (618, HEIGHT - 130))
    beatsText2 = SMALL_FONT.render(f'{BEATS}', True, WHITE)
    WIN.blit(beatsText2, (680, HEIGHT - 100))
    # +/- Beats buttons
    beatsAddRect = pygame.draw.rect(WIN, GRAY4, [810, HEIGHT - 150, 48, 48], 0, 5)
    addText2 = SMALL_FONT.render('+1', True, WHITE)
    WIN.blit(addText2, (820, HEIGHT - 140))
    beatsSubRect = pygame.draw.rect(WIN, GRAY4, [810, HEIGHT - 100, 48, 48], 0, 5)
    subText2 = SMALL_FONT.render('-1', True, WHITE)
    WIN.blit(subText2, (820, HEIGHT - 90))

    # Instrument collision buttons/rectangles:
    instrumentRects = []
    for i in range(INSTRUMENTS):
        rect = pygame.rect.Rect((0, i * 100), (220, 100))
        instrumentRects.append(rect)

    # Save Button:
    saveButton = pygame.draw.rect(WIN, GRAY4, [900, HEIGHT - 150, 200, 48], 0, 5)
    saveText = FONT.render('Save Beat', True, WHITE)
    WIN.blit(saveText, (920, HEIGHT - 135))
    # Load Button:
    loadButton = pygame.draw.rect(WIN, GRAY4, [900, HEIGHT - 100, 200, 48], 0, 5)
    loadText = FONT.render('Load Beat', True, WHITE)
    WIN.blit(loadText, (920, HEIGHT - 90))

    # Clear Board Button:
    clearButton = pygame.draw.rect(WIN, GRAY4, [1145, HEIGHT - 150, 210, 100], 0, 5)
    clearText = FONT.render('Clear Board', True, WHITE)
    WIN.blit(clearText, (1152, HEIGHT - 115))

    # Save/Load Menus:
    if SAVE_MENU: # save menu/state
        # Function call and saving buttons for event handlers:
       exitButton, savingButton, entryRectangle = drawSaveMenu(BEAT_NAME, TYPING) 
    if LOAD_MENU: # load menu/state
        # Function call and saving buttons for event handlers:
       exitButton, loadButton, deleteButton, loadedRectangle, loadedInfo = drawLoadMenu(INDEX) 

    # To handle change in number of beats:
    if BEAT_CHANGED:
        playSounds()
        BEAT_CHANGED = False

    # Event Handler:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # on 'X' click
            run = False

        # Grid button click handler:
        if event.type == pygame.MOUSEBUTTONDOWN and not SAVE_MENU and not LOAD_MENU:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    CLICKED[coords[1]][coords[0]] *= -1 # turns grid box on/off (1 or -1)

        # Menu button handler:
        if event.type == pygame.MOUSEBUTTONUP and not SAVE_MENU and not LOAD_MENU:

            # Play/Pause button handler:
            if playPause.collidepoint(event.pos):
                if PLAYING: # if already playing:
                    PLAYING = False # pause
                elif not PLAYING: # if paused:
                    PLAYING = True # play

            # BPM button handler:
            elif bpmAddRect.collidepoint(event.pos):
                BPM += 5 
            elif bpmSubRect.collidepoint(event.pos):
                BPM -= 5

            # Beats button handler:
            elif beatsAddRect.collidepoint(event.pos):
                BEATS += 1 
                # Add new column to the grid:
                for i in range(len(CLICKED)):
                    CLICKED[i].append(-1)
            elif beatsSubRect.collidepoint(event.pos):
                BEATS -= 1 
                # Subtract a column from the grid:
                for i in range(len(CLICKED)):
                    CLICKED[i].pop(-1)

            # Clear grid button:
            elif clearButton.collidepoint(event.pos):
                CLICKED = [[-1 for _ in range(BEATS)] for _ in range(INSTRUMENTS)]

            # Save/Load buttons:
            elif saveButton.collidepoint(event.pos):
                SAVE_MENU = True 
            elif loadButton.collidepoint(event.pos):
                LOAD_MENU = True

            # Instrument panel button handler:
            for i in range(len(instrumentRects)):
                if instrumentRects[i].collidepoint(event.pos):
                    ACTIVE_LIST[i] *= -1 # turns row off

        # Quit menu button:
        elif event.type == pygame.MOUSEBUTTONUP:
            if exitButton.collidepoint(event.pos):
                SAVE_MENU = False # close out of menu
                LOAD_MENU = False # close out of menu
                PLAYING = True # start playing
                BEAT_NAME = '' # reset beat name
                TYPING = False # exit typing mode

            # In load menu:
            if LOAD_MENU: 
                # Highlight selection:
                if loadedRectangle.collidepoint(event.pos):
                    INDEX = (event.pos[1] - 100) // 50

                # Delete beat button:
                if deleteButton.collidepoint(event.pos):
                    if 0 <= INDEX < len(SAVED_BEATS):
                        SAVED_BEATS.pop(INDEX)

                # Load beat button:
                if loadButton.collidepoint(event.pos):
                    if 0 <= INDEX < len(SAVED_BEATS):
                        # Load selected info:
                        BEATS = loadedInfo[0]
                        BPM = loadedInfo[1]
                        CLICKED = loadedInfo[2] # grid

                        INDEX = 100 # hide selection box
                        LOAD_MENU = False # close out of load menu

            # In save menu:
            if SAVE_MENU:
                # Text area box:
                if entryRectangle.collidepoint(event.pos):
                    if TYPING: # if already in typing mode:
                        TYPING = False # exit typing mode
                    elif not TYPING: # if not in typing mode
                        TYPING = True # enter typing mode

                # Save beat button:
                if savingButton.collidepoint(event.pos):
                    FILE = open('./saved_beats.txt', 'w') # open file in write mode

                    # Save beat using this format:
                    SAVED_BEATS.append(f'\nname: {BEAT_NAME}, beats: {BEATS}, bpm: {BPM}, selected: {CLICKED}')

                    # Overwrite save file:
                    for i in range(len(SAVED_BEATS)):
                        FILE.write(str(SAVED_BEATS[i]))

                    FILE.close() # close save file

                    # Reset to defaults:
                    SAVE_MENU = False
                    TYPING = False 
                    BEAT_NAME = ''

        # Adding text when typing:
        if event.type == pygame.TEXTINPUT and TYPING:
            BEAT_NAME += event.text

        # Backspace functionality in typing mode:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(BEAT_NAME) > 0 and TYPING:
                BEAT_NAME = BEAT_NAME[:-1]

    # Length of beats in grid (real time):
    beatLength = FPS * 60 // BPM # (fps * 60seconds) // bpm

    # Move active list while playing:
    if PLAYING:
        if ACTIVE_LENGTH < beatLength: # if active column is still on grid
            ACTIVE_LENGTH += 1 # move active column
        else:
            ACTIVE_LENGTH = 0 # move column to 0
            if ACTIVE_BEAT < BEATS - 1: # if beats were added to grid:
                ACTIVE_BEAT += 1  # add distance to active column
                BEAT_CHANGED = True 
            else:
                ACTIVE_BEAT = 0 # reset which beat is playing
                BEAT_CHANGED = True

    pygame.display.flip() # updates display

# Write deletions/changes to file on end of game loop:
FILE = open('./saved_beats.txt', 'w')
# Overwrite file with current list:
for i in range(len(SAVED_BEATS)):
    FILE.write(str(SAVED_BEATS[i]))
# Close save file:
FILE.close()

pygame.quit() # Quit game on end of game loop:
# drumDrum by Gesty Linaga
