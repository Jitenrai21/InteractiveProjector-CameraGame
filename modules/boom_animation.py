import pygame

def generate_boom_frames(base_image, num_frames=6, final_scale=1.5):
    frames = []
    base_width, base_height = base_image.get_size()

    for i in range(num_frames):
        # Calculate scale factor (grows up to final_scale)
        scale_factor = 1.0 + (final_scale - 1.0) * (i / (num_frames - 1))
        new_width = int(base_width * scale_factor)
        new_height = int(base_height * scale_factor)

        # Scale the image
        scaled_image = pygame.transform.smoothscale(base_image, (new_width, new_height))

        # Center the boom around original
        frame = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
        frame.blit(scaled_image, (0, 0))

        # Apply alpha fade
        alpha = int(255 * (1 - i / (num_frames - 1)))  # fades out
        frame.set_alpha(alpha)

        frames.append(frame)

    return frames
