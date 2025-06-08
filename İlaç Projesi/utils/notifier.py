import os
import time
from datetime import datetime
from typing import Dict, List
import schedule
from rich.console import Console
from rich.panel import Panel

console = Console()

class Notifier:
    def __init__(self, data_manager):
        """Bildirim yöneticisi sınıfının başlatıcısı.
        
        Args:
            data_manager: DataManager sınıfının bir örneği
        """
        self.data_manager = data_manager
        self.console = Console()
    
    def _make_sound(self) -> None:
        """Terminal üzerinden bildirim sesi çalar."""
        print('\a')  # Terminal bell
    
    def check_schedule(self) -> None:
        """Günlük programı kontrol eder ve bildirimleri gösterir."""
        today_schedule = self.data_manager.get_today_schedule()
        
        current_time = datetime.now().strftime("%H:%M")
        
        # Randevuları kontrol et
        for appointment in today_schedule["appointments"]:
            if appointment["time"] == current_time:
                self._notify_appointment(appointment)
        
        # İlaçları kontrol et
        for medication in today_schedule["medications"]:
            if medication["time"] == current_time:
                self._notify_medication(medication)
    
    def _notify_appointment(self, appointment: Dict) -> None:
        """Randevu bildirimi gösterir."""
        user = self.data_manager.get_user(appointment["user_id"])
        message = f"🏥 RANDEVU HATIRLATMASI\n\n"
        message += f"Hasta: {user['name']}\n"
        message += f"Saat: {appointment['time']}\n"
        message += f"Açıklama: {appointment['description']}"
        
        self.console.print(Panel(
            message,
            title="HealthTrack Bildirimi",
            style="bold green"
        ))
        self._make_sound()
    
    def _notify_medication(self, medication: Dict) -> None:
        """İlaç bildirimi gösterir."""
        user = self.data_manager.get_user(medication["user_id"])
        message = f"💊 İLAÇ HATIRLATMASI\n\n"
        message += f"Hasta: {user['name']}\n"
        message += f"İlaç: {medication['name']}\n"
        message += f"Saat: {medication['time']}\n"
        message += f"Sıklık: {medication['frequency']}"
        
        self.console.print(Panel(
            message,
            title="HealthTrack Bildirimi",
            style="bold blue"
        ))
        self._make_sound()
    
    def start_monitoring(self) -> None:
        """Bildirim sistemini başlatır ve sürekli çalışır."""
        schedule.every().minute.do(self.check_schedule)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)  # Her 30 saniyede bir kontrol et
        except KeyboardInterrupt:
            console.print("Bildirim sistemi durduruldu.", style="bold red") 