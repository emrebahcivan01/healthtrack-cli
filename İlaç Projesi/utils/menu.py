import inquirer
from rich.console import Console
from rich.table import Table
from datetime import datetime
from typing import Dict, List

console = Console()

class Menu:
    def __init__(self, data_manager):
        """Menü yöneticisi sınıfının başlatıcısı.
        
        Args:
            data_manager: DataManager sınıfının bir örneği
        """
        self.data_manager = data_manager
    
    def show_main_menu(self) -> str:
        """Ana menüyü gösterir ve kullanıcı seçimini döndürür."""
        questions = [
            inquirer.List('choice',
                message='Lütfen bir işlem seçin:',
                choices=[
                    ('1. Kullanıcı Ekle/Düzenle', '1'),
                    ('2. Randevu Yönetimi', '2'),
                    ('3. İlaç Takibi', '3'),
                    ('4. Günlük Özet', '4'),
                    ('5. Rapor Oluştur', '5'),
                    ('6. Ayarlar', '6'),
                    ('Çıkış', 'q')
                ],
            )
        ]
        answers = inquirer.prompt(questions)
        return answers['choice']
    
    def add_user_menu(self) -> Dict:
        """Kullanıcı ekleme menüsünü gösterir ve girilen bilgileri döndürür."""
        questions = [
            inquirer.Text('name', message='Hasta Adı:'),
            inquirer.Text('age', message='Yaş:'),
            inquirer.Text('health_status', message='Sağlık Durumu:')
        ]
        answers = inquirer.prompt(questions)
        return self.data_manager.add_user(
            answers['name'],
            int(answers['age']),
            answers['health_status']
        )
    
    def add_appointment_menu(self) -> Dict:
        """Randevu ekleme menüsünü gösterir."""
        users = self.data_manager.get_all_users()
        if not users:
            console.print("Önce bir kullanıcı eklemelisiniz!", style="bold red")
            return None
        
        user_choices = [(f"{user['name']} ({user['age']} yaş)", user['id']) for user in users]
        
        questions = [
            inquirer.List('user_id',
                message='Hasta seçin:',
                choices=user_choices
            ),
            inquirer.Text('date',
                message='Tarih (YYYY-MM-DD):',
                validate=lambda _, x: len(x.split('-')) == 3
            ),
            inquirer.Text('time',
                message='Saat (HH:MM):',
                validate=lambda _, x: len(x.split(':')) == 2
            ),
            inquirer.Text('description',
                message='Açıklama:'
            )
        ]
        
        answers = inquirer.prompt(questions)
        return self.data_manager.add_appointment(
            answers['user_id'],
            answers['date'],
            answers['time'],
            answers['description']
        )
    
    def add_medication_menu(self) -> Dict:
        """İlaç ekleme menüsünü gösterir."""
        users = self.data_manager.get_all_users()
        if not users:
            console.print("Önce bir kullanıcı eklemelisiniz!", style="bold red")
            return None
        
        user_choices = [(f"{user['name']} ({user['age']} yaş)", user['id']) for user in users]
        
        questions = [
            inquirer.List('user_id',
                message='Hasta seçin:',
                choices=user_choices
            ),
            inquirer.Text('name',
                message='İlaç adı:'
            ),
            inquirer.Text('time',
                message='Saat (HH:MM):',
                validate=lambda _, x: len(x.split(':')) == 2
            ),
            inquirer.List('frequency',
                message='Kullanım sıklığı:',
                choices=[
                    'Günde bir kez',
                    'Günde iki kez',
                    'Günde üç kez',
                    'Haftada bir kez',
                    'Gerektiğinde'
                ]
            )
        ]
        
        answers = inquirer.prompt(questions)
        return self.data_manager.add_medication(
            answers['user_id'],
            answers['name'],
            answers['time'],
            answers['frequency']
        )
    
    def show_daily_summary(self) -> None:
        """Günlük özeti gösterir."""
        schedule = self.data_manager.get_today_schedule()
        
        # Randevular tablosu
        appointments_table = Table(title="🏥 Bugünkü Randevular")
        appointments_table.add_column("Saat", style="cyan")
        appointments_table.add_column("Hasta", style="green")
        appointments_table.add_column("Açıklama", style="yellow")
        
        for apt in schedule["appointments"]:
            user = self.data_manager.get_user(apt["user_id"])
            appointments_table.add_row(
                apt["time"],
                user["name"],
                apt["description"]
            )
        
        # İlaçlar tablosu
        medications_table = Table(title="💊 Bugünkü İlaçlar")
        medications_table.add_column("Saat", style="cyan")
        medications_table.add_column("Hasta", style="green")
        medications_table.add_column("İlaç", style="yellow")
        medications_table.add_column("Sıklık", style="magenta")
        
        for med in schedule["medications"]:
            user = self.data_manager.get_user(med["user_id"])
            medications_table.add_row(
                med["time"],
                user["name"],
                med["name"],
                med["frequency"]
            )
        
        console.print("\n")
        console.print(appointments_table)
        console.print("\n")
        console.print(medications_table)
        console.print("\n") 