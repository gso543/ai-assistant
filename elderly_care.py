from flask import Blueprint, jsonify, request, current_app
from datetime import datetime, timedelta
import random


elderly_care_bp = Blueprint('elderly_care', __name__)

# محاكاة بيانات المراقبة
monitoring_data = {
    'system_status': 'active',
    'last_movement': datetime.now() - timedelta(minutes=5),
    'activity_level': 'normal',
    'fall_detected': False,
    'emergency_alerts': []
}

# محاكاة البيانات الصحية
health_data = {
    'sleep_hours': 7.5,
    'daily_activity': 'medium',
    'last_medication': datetime.now() - timedelta(hours=2),
    'heart_rate': 72,
    'activity_pattern': 'normal'
}

# سجل الأنشطة
activity_log = [
    {
        'timestamp': datetime.now() - timedelta(minutes=30),
        'message': 'تم رصد حركة طبيعية في غرفة المعيشة',
        'type': 'movement'
    },
    {
        'timestamp': datetime.now() - timedelta(hours=1, minutes=15),
        'message': 'تذكير بتناول الدواء - تم التأكيد',
        'type': 'medication'
    },
    {
        'timestamp': datetime.now() - timedelta(hours=1, minutes=45),
        'message': 'بداية النشاط اليومي',
        'type': 'activity'
    },
    {
        'timestamp': datetime.now() - timedelta(hours=4),
        'message': 'استيقاظ من النوم',
        'type': 'sleep'
    }
]

@elderly_care_bp.route('/monitoring', methods=['GET'])
def get_monitoring_data():
    """الحصول على بيانات المراقبة الحالية"""
    # محاكاة تحديث البيانات
    monitoring_data['last_movement'] = datetime.now() - timedelta(minutes=random.randint(1, 10))
    monitoring_data['activity_level'] = random.choice(['low', 'normal', 'high'])
    
    return jsonify({
        'system_status': monitoring_data['system_status'],
        'last_movement': monitoring_data['last_movement'].isoformat(),
        'activity_level': monitoring_data['activity_level'],
        'fall_detected': monitoring_data['fall_detected'],
        'emergency_alerts_count': len(monitoring_data['emergency_alerts'])
    })

@elderly_care_bp.route('/health', methods=['GET'])
def get_health_data():
    """الحصول على البيانات الصحية"""
    # محاكاة تحديث البيانات الصحية
    health_data['sleep_hours'] = round(6 + random.random() * 3, 1)
    health_data['daily_activity'] = random.choice(['low', 'medium', 'high', 'excellent'])
    health_data['heart_rate'] = random.randint(65, 85)
    
    return jsonify({
        'sleep_hours': health_data['sleep_hours'],
        'daily_activity': health_data['daily_activity'],
        'last_medication': health_data['last_medication'].isoformat(),
        'heart_rate': health_data['heart_rate'],
        'activity_pattern': health_data['activity_pattern']
    })

@elderly_care_bp.route('/activity-log', methods=['GET'])
def get_activity_log():
    """الحصول على سجل الأنشطة"""
    # تحويل التواريخ إلى نص قابل للقراءة
    formatted_log = []
    for entry in activity_log:
        formatted_log.append({
            'timestamp': entry['timestamp'].isoformat(),
            'message': entry['message'],
            'type': entry['type'],
            'time_ago': get_time_ago(entry['timestamp'])
        })
    
    return jsonify(formatted_log)

@elderly_care_bp.route('/emergency', methods=['POST'])
def trigger_emergency():
    """تفعيل تنبيه الطوارئ"""
    data = request.json
    alert = {
        'timestamp': datetime.now(),
        'message': data.get('message', 'تنبيه طوارئ عام'),
        'severity': data.get('severity', 'high'),
        'resolved': False
    }
    
    monitoring_data['emergency_alerts'].append(alert)
    
    # إضافة إلى سجل الأنشطة
    activity_log.insert(0, {
        'timestamp': datetime.now(),
        'message': f"تنبيه طوارئ: {alert['message']}",
        'type': 'emergency'
    })
    
    return jsonify({
        'status': 'success',
        'message': 'تم إرسال تنبيه الطوارئ بنجاح',
        'alert_id': len(monitoring_data['emergency_alerts']) - 1
    }), 201

@elderly_care_bp.route('/test-system', methods=['POST'])
def test_system():
    """اختبار النظام"""
    # محاكاة اختبار النظام
    test_results = {
        'monitoring_system': 'ok',
        'voice_assistant': 'ok',
        'emergency_alerts': 'ok',
        'database': 'ok',
        'timestamp': datetime.now().isoformat()
    }
    
    # إضافة إلى سجل الأنشطة
    activity_log.insert(0, {
        'timestamp': datetime.now(),
        'message': 'تم اختبار النظام بنجاح - جميع الأنظمة تعمل بشكل طبيعي',
        'type': 'system_test'
    })
    
    return jsonify({
        'status': 'success',
        'message': 'تم اختبار النظام بنجاح',
        'results': test_results
    })

@elderly_care_bp.route('/add-log', methods=['POST'])
def add_log_entry():
    """إضافة إدخال جديد إلى سجل الأنشطة"""
    data = request.json
    
    new_entry = {
        'timestamp': datetime.now(),
        'message': data.get('message', 'نشاط جديد'),
        'type': data.get('type', 'general')
    }
    
    activity_log.insert(0, new_entry)
    
    # الاحتفاظ بآخر 50 إدخال فقط
    if len(activity_log) > 50:
        activity_log.pop()
    
    return jsonify({
        'status': 'success',
        'message': 'تم إضافة الإدخال بنجاح'
    }), 201

def get_time_ago(timestamp):
    """حساب الوقت المنقضي منذ الحدث"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"منذ {diff.days} يوم"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"منذ {hours} ساعة"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"منذ {minutes} دقيقة"
    else:
        return "الآن"

@elderly_care_bp.route("/recommendations", methods=["GET"])
def get_health_recommendations():
    """الحصول على توصيات صحية مخصصة"""
    # هنا يمكننا استخدام بيانات حقيقية من قاعدة البيانات أو محاكاة بيانات المستخدم
    # For demonstration, we use some fixed values or random values
    age = random.randint(65, 95)
    sleep_hours = round(6 + random.random() * 3, 1)
    daily_activity_level = random.choice(["low", "medium", "high"])
    heart_rate = random.randint(60, 100)
    medication_adherence = round(random.uniform(0.5, 1.0), 2)
    fall_risk_score = round(random.uniform(0.0, 1.0), 2)

    recommender = current_app.health_recommender # Access the recommender from current_app
    recommendation = recommender.get_recommendations(
        age=age, 
        sleep_hours=sleep_hours, 
        daily_activity_level=daily_activity_level, 
        heart_rate=heart_rate, 
        medication_adherence=medication_adherence, 
        fall_risk_score=fall_risk_score
    )
    
    return jsonify({
        "age": age,
        "sleep_hours": sleep_hours,
        "daily_activity_level": daily_activity_level,
        "heart_rate": heart_rate,
        "medication_adherence": medication_adherence,
        "fall_risk_score": fall_risk_score,
        "recommendation": recommendation
    })

@elderly_care_bp.route("/voice-command", methods=["POST"])
def voice_command_api():
    """معالجة أمر صوتي (نصي) من المساعد الصوتي المحاكي."""
    data = request.json
    command_text = data.get("command")

    if not command_text:
        return jsonify({"error": "No command text provided"}), 400

    try:
        assistant = current_app.voice_assistant
        # Simulate assistant processing and speaking
        # For simplicity, we'll just return the processed command result
        # In a real scenario, the assistant.speak() would output audio
        response_message = assistant.process_command(command_text)
        
        return jsonify({
            "status": "success",
            "response": response_message # This will be the simulated spoken text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@elderly_care_bp.route("/dashboard-stats", methods=["GET"])
def get_dashboard_stats():
    """الحصول على إحصائيات شاملة للوحة التحكم"""
    # محاكاة تحديث البيانات
    monitoring_data["last_movement"] = datetime.now() - timedelta(minutes=random.randint(1, 10))
    monitoring_data["activity_level"] = random.choice(["low", "normal", "high"])
    health_data["sleep_hours"] = round(6 + random.random() * 3, 1)
    health_data["daily_activity"] = random.choice(["low", "medium", "high", "excellent"])
    health_data["heart_rate"] = random.randint(65, 85)

    # Get a recommendation
    recommender = current_app.health_recommender
    current_recommendation = recommender.get_recommendations(
        age=75, # Example fixed age
        sleep_hours=health_data["sleep_hours"],
        daily_activity_level=health_data["daily_activity"],
        heart_rate=health_data["heart_rate"],
        medication_adherence=0.9, # Example fixed adherence
        fall_risk_score=0.5 # Example fixed fall risk
    )

    return jsonify({
        "monitoring": {
            "system_status": monitoring_data["system_status"],
            "last_movement": get_time_ago(monitoring_data["last_movement"]),
            "activity_level": monitoring_data["activity_level"],
            "fall_detected": monitoring_data['fall_detected']
        },
        "health": {
            "sleep_hours": health_data["sleep_hours"],
            "daily_activity": health_data["daily_activity"],
            "last_medication": get_time_ago(health_data["last_medication"]),
            "heart_rate": health_data["heart_rate"]
        },
        "emergency": {
            "active_alerts": len([alert for alert in monitoring_data["emergency_alerts"] if not alert.get("resolved", False)]),
            "total_alerts": len(monitoring_data["emergency_alerts"]),
            "last_safety_check": get_time_ago(datetime.now() - timedelta(minutes=10))
        },
        "activity_summary": {
            "total_entries": len(activity_log),
            "recent_entries": len([entry for entry in activity_log if (datetime.now() - entry["timestamp"]).days == 0])
        },
        "recommendation": current_recommendation
    })
