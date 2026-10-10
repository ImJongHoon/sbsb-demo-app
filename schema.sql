-- PostgreSQL Schema for sbsb-demo-app

CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS deploy_logs (
    id SERIAL PRIMARY KEY,
    event VARCHAR(100) NOT NULL,
    details TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed Initial Data
INSERT INTO items (id, title, category) VALUES
    (1, '온프레미스 Docker 볼륨 마운트 테스트', 'infra'),
    (2, 'PostgreSQL 데이터베이스 자동 연동 검증', 'database'),
    (3, 'SBSB 원클릭 무중단 배포 확인', 'deployment')
ON CONFLICT (id) DO NOTHING;

INSERT INTO deploy_logs (id, event, details) VALUES
    (1, 'SYSTEM_INIT', '데이터베이스 스키마가 성공적으로 초기화되었습니다.')
ON CONFLICT (id) DO NOTHING;