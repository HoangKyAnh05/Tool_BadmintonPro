import React, { useState, useEffect } from 'react';
import { TrainingMode } from '../../types';
import { storageService, LifetimeStats } from '../../services/storage';
import { 
  Flame, 
  Trophy, 
  Zap, 
  ArrowRight, 
  Compass, 
  Play, 
  Target,
  Footprints,
  BookOpen,
  Layers,
  Sparkles,
  Camera,
  Activity,
  Star
} from 'lucide-react';
import { VideoSection } from '../Video/VideoSection';
import { DailyChallengeCard } from '../DailyChallenge/DailyChallengeCard';
import { DailyWorkout } from '../../data/dailyPlan100';

interface HomeDashboardProps {
  onSelectMode: (mode: TrainingMode) => void;
  onQuickStart: () => void;
  onOpenRecorder?: () => void;
  onOpenVideoHub?: () => void;
}

export const HomeDashboard: React.FC<HomeDashboardProps> = ({
  onSelectMode,
  onQuickStart,
  onOpenRecorder,
  onOpenVideoHub
}) => {
  const [lifetime, setLifetime] = useState<LifetimeStats>(() => storageService.loadLifetimeStats());
  const [dailyProgress, setDailyProgress] = useState(() => storageService.loadDailyProgress());
  const [expLevel, setExpLevel] = useState<'BEGINNER' | 'ADVANCED'>(() => storageService.loadUserExperienceLevel());

  useEffect(() => {
    setLifetime(storageService.loadLifetimeStats());
    setDailyProgress(storageService.loadDailyProgress());
    setExpLevel(storageService.loadUserExperienceLevel());
  }, []);

  const handleToggleExpLevel = (level: 'BEGINNER' | 'ADVANCED') => {
    setExpLevel(level);
    storageService.saveUserExperienceLevel(level);
  };

  const handleCompleteDay = (dayNumber: number) => {
    const updated = storageService.completeDayWorkout(dayNumber);
    setDailyProgress(updated);
  };

  const handleSelectWorkout = (workout: DailyWorkout) => {
    onSelectMode(workout.suggestedMode);
  };

  const trainingCards: {
    mode: TrainingMode;
    title: string;
    tagline: string;
    desc: string;
    colorClass: string;
    badge: string;
    emoji: string;
  }[] = [
    {
      mode: 'TAY',
      title: 'KỸ THUẬT VỢT (TAY)',
      tagline: 'Phản xạ tay & tiếp xúc cầu',
      desc: 'Rèn luyện phản xạ đón cầu trên lưới, tạt cầu ngang mặt, vồ cầu và phòng thủ đập.',
      colorClass: 'card-tay',
      badge: 'Chuyên môn tay',
      emoji: '🎯'
    },
    {
      mode: 'CHÂN',
      title: 'BỘ PHÁP DI CHUYỂN (CHÂN)',
      tagline: 'Bộ chân & nhịp bước trên sân',
      desc: 'Rèn luyện split-step, bước lunge dài lên lưới, bật lùi chéo góc và bước scissor kick.',
      colorClass: 'card-chan',
      badge: 'Bộ chân di chuyển',
      emoji: '🦶'
    },
    {
      mode: 'TAY + CHÂN',
      title: 'PHỐI HỢP TAY & CHÂN',
      tagline: 'Đồng bộ động tác & bộ vị',
      desc: 'Đồng bộ nhịp tiếp đất chân thuận cùng thời điểm tiếp xúc cầu và nhanh chóng hồi tâm.',
      colorClass: 'card-tay-chan',
      badge: 'Phối hợp nhịp nhàng',
      emoji: '⚡'
    },
    {
      mode: 'LÝ THUYẾT',
      title: 'LÝ THUYẾT CHIẾN THUẬT',
      tagline: 'Phân tích tình huống thi đấu',
      desc: 'Bộ câu hỏi xử lý tình huống thực tế: đánh đơn, đánh đôi, đọc ý đồ đối phương.',
      colorClass: 'card-theory',
      badge: 'Tư duy chiến thuật',
      emoji: '🧠'
    },
    {
      mode: 'TOÀN BỘ',
      title: 'BÀI TẬP TỔNG HỢP',
      tagline: 'Mô phỏng trận đấu thực tế',
      desc: 'Trộn ngẫu nhiên kỹ thuật, bộ chân và phản xạ liên hoàn tạo áp lực như khi thi đấu.',
      colorClass: 'card-all',
      badge: 'Mô phỏng thi đấu',
      emoji: '🏆'
    }
  ];

  return (
    <div className="home-dashboard animate-fade-in kid-friendly-home">
      {/* Friendly Top Welcome Strip */}
      <div className="kid-welcome-header animate-fade-in">
        <div className="kid-welcome-content">
          <div className="kid-welcome-pill">
            <Sparkles size={16} className="text-amber animate-spin-slow" />
            <span>HỌC VIỆN CẦU LÔNG THÔNG MINH • XEM VIDEO & TẬP LUYỆN DỄ DÀNG</span>
          </div>
          <h1 className="kid-welcome-title">
            HÃY XEM VIDEO & <span className="highlight-text">TẬP CÙNG HUẤN LUYỆN VIÊN</span>!
          </h1>
          <p className="kid-welcome-subtitle">
            Hơn 330 bài học video sinh động, chuẩn kỹ thuật BWF. Bấm chọn bài học bên dưới để xem ngay!
          </p>
        </div>

        <div className="kid-quick-stats-strip">
          <div className="kid-stat-chip">
            <Flame size={20} className="text-amber" />
            <div>
              <strong>{lifetime.streakDays} ngày</strong>
              <small>Chuỗi tập</small>
            </div>
          </div>
          <div className="kid-stat-chip">
            <Trophy size={20} className="text-emerald" />
            <div>
              <strong>{lifetime.totalRoundsCompleted} lượt</strong>
              <small>Đã hoàn thành</small>
            </div>
          </div>
          <div className="kid-stat-chip">
            <Zap size={20} className="text-cyan" />
            <div>
              <strong>{lifetime.bestReactionTime > 0 ? `${lifetime.bestReactionTime}s` : '--'}</strong>
              <small>Kỷ lục phản xạ</small>
            </div>
          </div>
        </div>
      </div>

      {/* ========================================================== */}
      {/* 1. KHO VIDEO TRÊN CÙNG (VIDEO SECTION ON TOP)               */}
      {/* ========================================================== */}
      <VideoSection initialLevel={expLevel === 'BEGINNER' ? 'Cơ bản' : 'ALL'} />

      {/* ========================================================== */}
      {/* 2. KHỐI BẮT ĐẦU TẬP PHẢN XẠ NHANH (1 BẤM TẬP NGAY)          */}
      {/* ========================================================== */}
      <div className="kid-quickstart-cta-banner animate-scale-up">
        <div className="cta-banner-left">
          <div className="cta-tag">⚡ TỰ ĐỘNG PHẢN XẠ THEO ĐÈN TÍN HIỆU</div>
          <h2>BẮT ĐẦU BÀI TẬP PHẢN XẠ 9 Ô SÂN</h2>
          <p>Nhìn đèn tín hiệu xuất hiện trên sân, bật bước di chuyển và thực hiện đúng kỹ thuật!</p>
          
          <div className="cta-exp-selector">
            <span className="exp-label">Chế độ của bé:</span>
            <button
              className={`btn-exp-chip ${expLevel === 'BEGINNER' ? 'active-beginner' : ''}`}
              onClick={() => handleToggleExpLevel('BEGINNER')}
            >
              🌱 Bé Mới Tập (Tốc độ nhẹ nhàng)
            </button>
            <button
              className={`btn-exp-chip ${expLevel === 'ADVANCED' ? 'active-advanced' : ''}`}
              onClick={() => handleToggleExpLevel('ADVANCED')}
            >
              ⚡ Bé Nâng Cao (Bứt tốc thi đấu)
            </button>
          </div>
        </div>

        <div className="cta-banner-right">
          <button className="btn-kid-mega-start" onClick={onQuickStart}>
            <Play size={32} fill="currentColor" className="animate-pulse" />
            <div className="start-text-col">
              <span className="mega-title">BẤM ĐÂY TẬP NGAY!</span>
              <span className="mega-subtitle">Tự động đếm nhịp & Hướng dẫn âm thanh</span>
            </div>
          </button>
          
          {onOpenRecorder && (
            <button className="btn-kid-record-cam" onClick={onOpenRecorder}>
              <Camera size={18} className="text-danger" />
              <span>Quay video bé tập</span>
            </button>
          )}
        </div>
      </div>

      {/* ========================================================== */}
      {/* 3. PHẦN CHƯƠNG TRÌNH HUẤN LUYỆN (5 CHẾ ĐỘ THỰC CHIẾN)      */}
      {/* ========================================================== */}
      <div className="modes-section kid-friendly-modes">
        <div className="section-title-wrap">
          <div>
            <span className="section-eyebrow">CHƯƠNG TRÌNH HUẤN LUYỆN BÀI BẢN</span>
            <h2 className="section-title">CHỌN NỘI DUNG TẬP LUYỆN</h2>
          </div>
          <span className="section-count">5 CHẾ ĐỘ RÈN LUYỆN</span>
        </div>

        <div className="cards-grid">
          {trainingCards.map((c) => (
            <div
              key={c.mode}
              className={`mode-card ${c.colorClass} kid-mode-card`}
              onClick={() => onSelectMode(c.mode)}
              role="button"
              tabIndex={0}
            >
              <div className="card-top-row">
                <div className="card-mode-icon-wrap">
                  {c.mode === 'TAY' && <Target size={24} className="text-cyan" />}
                  {c.mode === 'CHÂN' && <Footprints size={24} className="text-lime" />}
                  {c.mode === 'TAY + CHÂN' && <Zap size={24} className="text-amber" />}
                  {c.mode === 'LÝ THUYẾT' && <BookOpen size={24} className="text-purple" />}
                  {c.mode === 'TOÀN BỘ' && <Layers size={24} className="text-emerald" />}
                </div>
                <span className="card-badge">{c.badge}</span>
              </div>

              <h3 className="card-title">
                <span className="card-emoji">{c.emoji}</span> {c.title}
              </h3>
              <p className="card-tagline">{c.tagline}</p>
              <p className="card-desc">{c.desc}</p>

              <div className="card-footer">
                <span className="footer-action-text">Bấm vào đây để tập</span>
                <div className="circle-arrow">
                  <ArrowRight size={16} />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ========================================================== */}
      {/* 4. KẾ HOẠCH THỬ THÁCH 100 NGÀY                            */}
      {/* ========================================================== */}
      <DailyChallengeCard
        progress={dailyProgress}
        onSelectWorkout={handleSelectWorkout}
        onCompleteDay={handleCompleteDay}
      />

      {/* ========================================================== */}
      {/* 5. SƠ ĐỒ 9 VỊ TRÍ CHIẾN LƯỢC TRÊN SÂN                      */}
      {/* ========================================================== */}
      <div className="court-explainer-banner kid-court-banner">
        <div className="explainer-left">
          <Compass size={36} className="text-cyan" />
          <div>
            <h3>SƠ ĐỒ 9 VỊ TRÍ CHIẾN LƯỢC TRÊN SÂN (3×3)</h3>
            <p>
              Hệ thống chia toàn bộ nửa sân thi đấu thành 9 ô phản xạ: 3 vị trí Lưới (1,2,3), 3 vị trí Trung tâm (4,5,6), và 3 vị trí Cuối sân (7,8,9).
            </p>
          </div>
        </div>
        <div className="explainer-right">
          <span className="court-badge">Chuẩn Quốc Tế BWF</span>
        </div>
      </div>
    </div>
  );
};

export default HomeDashboard;
