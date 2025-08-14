from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController()
Sky()

spawn_point = Vec3(0, 10, 0)

# โหลด texture
block_textures = ['grass.png', 'stone.png', 'wood.png']
current_block = 0

# พื้นดิน
boxes = []
for i in range(20):
    for j in range(20):
        box = Button(color=color.white, model='cube', position=(j, 0, i),
                     texture='grass.png', parent=scene, origin_y=0.5)
        boxes.append(box)

# Toolbars
toolbar = []
toolbar_frame = Entity(model='quad', color=color.black66, scale=(1.2, 0.15), position=(0, -0.45), parent=camera.ui)

for i in range(len(block_textures)):
    slot = Entity(model='quad', texture=block_textures[i], scale=(0.09, 0.09),
                  position=(-0.42 + i*0.11, -0.45), parent=camera.ui)
    toolbar.append(slot)

# กรอบไฮไลต์ขอบหนา
selector = Entity(model=Mesh(vertices=[Vec3(-0.05, -0.05, 0), Vec3(-0.05, 0.05, 0),
                                       Vec3(0.05, 0.05, 0), Vec3(0.05, -0.05, 0)],
                             mode='line'), color=color.azure,
                  scale=(1.2, 1.2), parent=toolbar[0])

def input(key):
    global current_block

    # Scroll Mouse
    if key == 'scroll up':
        current_block = (current_block + 1) % len(block_textures)
    if key == 'scroll down':
        current_block = (current_block - 1) % len(block_textures)

    # กดเลข 1-9
    if key.isdigit():
        index = int(key) - 1
        if 0 <= index < len(block_textures):
            current_block = index

    # สร้าง / ลบ block
    for box in boxes:
        if box.hovered:
            if key == 'right mouse down':
                new_pos = box.position + mouse.normal
                if not any(b.position == new_pos for b in boxes):
                    new = Button(color=color.white, model='cube', position=new_pos,
                                 texture=block_textures[current_block], parent=scene, origin_y=0.5)
                    boxes.append(new)

            if key == 'left mouse down':
                boxes.remove(box)
                destroy(box)

fall_time = None
def update():
    global fall_time
    selector.position = toolbar[current_block].position

    if player.y < -10:
        if fall_time is None:
            fall_time = time.time()
    if fall_time is not None and time.time() - fall_time > 5:
        player.position = spawn_point
        player.velocity = Vec3(0, 0, 0)
        fall_time = None
  
  

app.run()
