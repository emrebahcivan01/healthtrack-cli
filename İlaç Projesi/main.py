import typer
import threading
from rich.console import Console
from utils.data_manager import DataManager
from utils.menu import Menu
from utils.notifier import Notifier

app = typer.Typer()
console = Console()

LOGO = """
╭─────────────────────────────────╮
│     🏥 HealthTrack v1.0 🏥      │
│   İlaç ve Randevu Asistanı     │
╰─────────────────────────────────╯
"""

def start_notification_thread(notifier: Notifier) -> None:
    """Bildirim sistemini ayrı bir thread'de başlatır."""
    notifier.start_monitoring()

@app.command()
def main(
    today: bool = typer.Option(False, "--today", help="Sadece bugünkü programı göster"),
    export: bool = typer.Option(False, "--export", help="Rapor oluştur")
):
    """HealthTrack - İlaç ve Randevu Takip Asistanı"""
    console.print(LOGO, style="bold blue")
    
    data_manager = DataManager()
    menu = Menu(data_manager)
    notifier = Notifier(data_manager)
    
    # Bildirim sistemini başlat
    notification_thread = threading.Thread(
        target=start_notification_thread,
        args=(notifier,),
        daemon=True
    )
    notification_thread.start()
    
    # --today flag'i kontrol et
    if today:
        menu.show_daily_summary()
        return
    
    # --export flag'i kontrol et
    if export:
        console.print("Rapor oluşturuluyor...", style="yellow")
        # TODO: Rapor oluşturma fonksiyonu eklenecek
        return
    
    # Ana menü döngüsü
    while True:
        choice = menu.show_main_menu()
        
        if choice == '1':
            user = menu.add_user_menu()
            if user:
                console.print(f"✅ Kullanıcı başarıyla eklendi: {user['name']}", style="bold green")
        
        elif choice == '2':
            appointment = menu.add_appointment_menu()
            if appointment:
                console.print("✅ Randevu başarıyla eklendi!", style="bold green")
        
        elif choice == '3':
            medication = menu.add_medication_menu()
            if medication:
                console.print("✅ İlaç başarıyla eklendi!", style="bold green")
        
        elif choice == '4':
            menu.show_daily_summary()
        
        elif choice == '5':
            console.print("Rapor oluşturuluyor...", style="yellow")
            # TODO: Rapor oluşturma fonksiyonu eklenecek
        
        elif choice == '6':
            console.print("Ayarlar menüsü yakında eklenecek...", style="yellow")
        
        elif choice == 'q':
            console.print("\nSağlıklı günler dileriz! 👋", style="bold blue")
            break

if __name__ == "__main__":
    app() 