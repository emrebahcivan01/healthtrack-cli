import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class DataManager:
    def __init__(self, file_path: str = "data/health_data.json"):
        """Veri yöneticisi sınıfının başlatıcısı.
        
        Args:
            file_path (str): JSON dosyasının yolu
        """
        self.file_path = file_path
        self._ensure_data_file()
        
    def _ensure_data_file(self) -> None:
        """Veri dosyasının varlığını kontrol eder ve yoksa oluşturur."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            self._save_data({
                "users": [],
                "appointments": [],
                "medications": []
            })
    
    def _load_data(self) -> Dict:
        """Veri dosyasından verileri yükler."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_data(self, data: Dict) -> None:
        """Verileri dosyaya kaydeder."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def add_user(self, name: str, age: int, health_status: str) -> Dict:
        """Yeni kullanıcı ekler.
        
        Args:
            name (str): Kullanıcı adı
            age (int): Yaş
            health_status (str): Sağlık durumu
        
        Returns:
            Dict: Eklenen kullanıcı bilgileri
        """
        data = self._load_data()
        user = {
            "id": len(data["users"]) + 1,
            "name": name,
            "age": age,
            "health_status": health_status,
            "created_at": datetime.now().isoformat()
        }
        data["users"].append(user)
        self._save_data(data)
        return user
    
    def add_appointment(self, user_id: int, date: str, time: str, description: str) -> Dict:
        """Yeni randevu ekler."""
        data = self._load_data()
        appointment = {
            "id": len(data["appointments"]) + 1,
            "user_id": user_id,
            "date": date,
            "time": time,
            "description": description,
            "created_at": datetime.now().isoformat()
        }
        data["appointments"].append(appointment)
        self._save_data(data)
        return appointment
    
    def add_medication(self, user_id: int, name: str, time: str, frequency: str) -> Dict:
        """Yeni ilaç ekler."""
        data = self._load_data()
        medication = {
            "id": len(data["medications"]) + 1,
            "user_id": user_id,
            "name": name,
            "time": time,
            "frequency": frequency,
            "created_at": datetime.now().isoformat()
        }
        data["medications"].append(medication)
        self._save_data(data)
        return medication
    
    def get_today_schedule(self, user_id: Optional[int] = None) -> Dict:
        """Bugünkü randevu ve ilaçları getirir."""
        data = self._load_data()
        today = datetime.now().strftime("%Y-%m-%d")
        
        today_appointments = [
            apt for apt in data["appointments"]
            if apt["date"] == today and (user_id is None or apt["user_id"] == user_id)
        ]
        
        today_medications = [
            med for med in data["medications"]
            if user_id is None or med["user_id"] == user_id
        ]
        
        return {
            "appointments": today_appointments,
            "medications": today_medications
        }
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Kullanıcı bilgilerini getirir."""
        data = self._load_data()
        for user in data["users"]:
            if user["id"] == user_id:
                return user
        return None
    
    def get_all_users(self) -> List[Dict]:
        """Tüm kullanıcıları getirir."""
        data = self._load_data()
        return data["users"] 