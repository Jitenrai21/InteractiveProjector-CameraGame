"""
Audio processing thread for handling sound effects without blocking main game loop.
Manages sound playback with queuing and volume control.
"""
import threading
import pygame
import time
import os
from queue import Queue, Empty
from typing import Dict, Optional
from .threaded_game_state import ThreadSafeGameState


class AudioManager(threading.Thread):
    """
    Dedicated thread for audio processing and sound effect management.
    Handles sound loading, playback queuing, and volume control.
    """
    
    def __init__(self, game_state: ThreadSafeGameState, base_dir: str):
        super().__init__(name="AudioManager")
        self.daemon = True
        
        self.game_state = game_state
        self.base_dir = base_dir
        
        # Audio queue for non-blocking playback
        self.audio_queue = Queue(maxsize=20)
        
        # Loaded sounds cache
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        
        # Audio settings
        self.master_volume = 0.7
        self.sfx_volume = 1.0
        self.music_volume = 0.5
        
        # Thread control
        self.running = True
        
        # Initialize pygame mixer if not already done
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Load common sound effects
        self._preload_sounds()
    
    def _preload_sounds(self):
        """Preload commonly used sound effects"""
        sound_files = {
            'pop': 'balloon-pop.mp3',
            'miss': 'miss.mp3',
            'pop_wav': 'pop.wav'  # Alternative pop sound
        }
        
        for sound_name, filename in sound_files.items():
            self._load_sound(sound_name, filename)
    
    def _load_sound(self, sound_name: str, filename: str) -> bool:
        """Load a sound file and cache it"""
        try:
            path = os.path.join(self.base_dir, "assets", filename)
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.sfx_volume * self.master_volume)
                self.sounds[sound_name] = sound
                print(f"Loaded sound: {sound_name}")
                return True
            else:
                print(f"Warning: Sound file not found: {path}")
        except Exception as e:
            print(f"Error: Failed to load sound {filename}: {e}")
        return False
    
    def run(self):
        """Main audio processing loop"""
        print("Audio manager thread started")
        
        while self.running and self.game_state.running:
            try:
                # Process audio queue
                try:
                    audio_request = self.audio_queue.get(timeout=0.1)
                    self._process_audio_request(audio_request)
                except Empty:
                    continue
                    
            except Exception as e:
                print(f"Error in audio manager thread: {e}")
                time.sleep(0.1)

        print("Audio manager thread stopped")

    def _process_audio_request(self, request: dict):
        """Process an audio playback request"""
        try:
            sound_name = request.get('sound')
            volume = request.get('volume', 1.0)
            priority = request.get('priority', 'normal')
            
            if sound_name in self.sounds:
                sound = self.sounds[sound_name]
                
                # Apply volume
                final_volume = volume * self.sfx_volume * self.master_volume
                sound.set_volume(final_volume)
                
                # Play sound
                if priority == 'high' or pygame.mixer.get_busy() < 3:  # Limit concurrent sounds
                    sound.play()
                
        except Exception as e:
            print(f"Error processing audio request: {e}")
    
    # Public interface methods
    def play_sound(self, sound_name: str, volume: float = 1.0, priority: str = 'normal'):
        """
        Queue a sound for playback (non-blocking).
        
        Args:
            sound_name: Name of the preloaded sound
            volume: Volume multiplier (0.0 to 1.0)
            priority: 'normal' or 'high' priority
        """
        try:
            request = {
                'sound': sound_name,
                'volume': volume,
                'priority': priority
            }
            self.audio_queue.put_nowait(request)
        except:
            pass  # Queue might be full, skip sound
    
    def play_pop_sound(self, volume: float = 1.0):
        """Play balloon pop sound effect"""
        self.play_sound('pop', volume, priority='high')
    
    def play_miss_sound(self, volume: float = 0.8):
        """Play miss sound effect"""
        self.play_sound('miss', volume, priority='normal')
    
    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        self._update_all_volumes()
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        self._update_all_volumes()
    
    def _update_all_volumes(self):
        """Update volume for all loaded sounds"""
        final_volume = self.sfx_volume * self.master_volume
        for sound in self.sounds.values():
            sound.set_volume(final_volume)
    
    def stop(self):
        """Stop the audio manager thread"""
        self.running = False
        pygame.mixer.stop()  # Stop all currently playing sounds
    
    def get_debug_info(self) -> dict:
        """Get debug information for monitoring"""
        return {
            'loaded_sounds': list(self.sounds.keys()),
            'queue_size': self.audio_queue.qsize(),
            'master_volume': self.master_volume,
            'sfx_volume': self.sfx_volume,
            'running': self.running,
            'mixer_busy': pygame.mixer.get_busy()
        }