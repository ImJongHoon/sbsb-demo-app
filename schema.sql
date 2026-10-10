-- SQLite Schema for sbsb-demo-app

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS deploy_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT NOT NULL,
    details TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed Initial Data
INSERT OR IGNORE INTO items (id, title, category) VALUES
    (1, '온프레미스 Docker 볼륨 마운트 테스트', 'infra'),
    (2, 'SQLite 데이터베이스 파일 입출력 검증', 'database'),
    (3, 'SBSB 원클릭 무중단 배포 확인', 'deployment');

INSERT OR IGNORE INTO deploy_logs (id, event, details) VALUES
    (1, 'SYSTEM_INIT', '데이터베이스 스키마가 성공적으로 초기화되었습니다.');
