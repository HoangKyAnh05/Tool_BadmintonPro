import React, { useState, useEffect, useMemo, useRef } from 'react';
import { TACTICS_VIDEOS } from '../../data/videos';
import { TacticsVideo, VideoCategory, SkillLevel } from '../../types';
import { storageService } from '../../services/storage';
import { VideoPlayerModal } from './VideoPlayerModal';
import { EditYouTubeLinkModal, extractYouTubeId, extractTikTokId, isTikTokUrl } from './EditYouTubeLinkModal';
import { YouTubeGuideModal } from './YouTubeGuideModal';
import { BatchImportExportModal } from './BatchImportExportModal';
import { 
  Tv, 
  Play, 
  CheckCircle2, 
  Search, 
  Sparkles,
  ChevronLeft,
  ChevronRight,
  Maximize2,
  Settings,
  Flame,
  Star,
  Zap,
  Volume2,
  RefreshCw,
  Award
} from 'lucide-react';
import { Youtube } from './YoutubeIcon';

type MainTabGroup = 
  | 'ALL' 
  | 'CORNERS' 
  | 'BO_PHAP' 
  | 'DI_CHUYEN' 
  | 'CHEM_CAU' 
  | 'JUMP_SMASH' 
  | 'VE_TRAI_TAY' 
  | 'PHAN_TAT_THU' 
  | 'MATCHES';

type LevelFilter = 'ALL' | SkillLevel;

const CATEGORY_TABS: { key: MainTabGroup; label: string; icon: string; countLabel?: string }[] = [
  { key: 'ALL', label: 'Tất cả video', icon: '🎬' },
  { key: 'CORNERS', label: '9 Ô trên sân', icon: '🎯' },
  { key: 'BO_PHAP', label: 'Bộ pháp', icon: '🦶' },
  { key: 'DI_CHUYEN', label: 'Di chuyển', icon: '🏃' },
  { key: 'CHEM_CAU', label: 'Chém & Cắt cầu', icon: '🌪️' },
  { key: 'JUMP_SMASH', label: 'Jump Smash', icon: '🚀' },
  { key: 'VE_TRAI_TAY', label: 'Ve trái tay', icon: '🏸' },
  { key: 'PHAN_TAT_THU', label: 'Phản tạt & Thủ', icon: '🛡️' },
  { key: 'MATCHES', label: 'Thi đấu thực tế', icon: '🏆' },
];

const CORNER_PILLS: { key: VideoCategory; label: string; num: number }[] = [
  { key: 'POS_1', label: 'Ô 1: Lưới Trái', num: 1 },
  { key: 'POS_2', label: 'Ô 2: Lưới Giữa', num: 2 },
  { key: 'POS_3', label: 'Ô 3: Lưới Phải', num: 3 },
  { key: 'POS_4', label: 'Ô 4: TT Trái', num: 4 },
  { key: 'POS_5', label: 'Ô 5: Tâm Sân', num: 5 },
  { key: 'POS_6', label: 'Ô 6: TT Phải', num: 6 },
  { key: 'POS_7', label: 'Ô 7: Đáy Trái', num: 7 },
  { key: 'POS_8', label: 'Ô 8: Đáy Giữa', num: 8 },
  { key: 'POS_9', label: 'Ô 9: Đáy Phải', num: 9 },
];

const MATCH_PILLS: { key: VideoCategory; label: string }[] = [
  { key: 'DON_NAM', label: 'Đơn Nam' },
  { key: 'DOI_NAM', label: 'Đôi Nam' },
  { key: 'DON_NU', label: 'Đơn Nữ' },
  { key: 'DOI_NU', label: 'Đôi Nữ' },
];

interface VideoSectionProps {
  initialLevel?: SkillLevel | 'ALL';
}

export const VideoSection: React.FC<VideoSectionProps> = ({ initialLevel }) => {
  const [activeGroup, setActiveGroup] = useState<MainTabGroup>('ALL');
  const [activeCorner, setActiveCorner] = useState<VideoCategory | 'ALL'>('ALL');
  const [activeMatch, setActiveMatch] = useState<VideoCategory | 'ALL'>('ALL');
  const [levelFilter, setLevelFilter] = useState<LevelFilter>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  
  // Featured Inline Video Stage
  const [currentVideo, setCurrentVideo] = useState<TacticsVideo>(() => TACTICS_VIDEOS[0]);
  const [isAutoNext, setIsAutoNext] = useState<boolean>(true);
  const [isPlayingStage, setIsPlayingStage] = useState<boolean>(true);

  // Modals
  const [theaterModalVideo, setTheaterModalVideo] = useState<TacticsVideo | null>(null);
  const [isEditModalOpen, setIsEditModalOpen] = useState<boolean>(false);
  const [editingVideo, setEditingVideo] = useState<TacticsVideo | null>(null);
  const [isGuideModalOpen, setIsGuideModalOpen] = useState<boolean>(false);
  const [isBatchModalOpen, setIsBatchModalOpen] = useState<boolean>(false);
  const [showAdminTools, setShowAdminTools] = useState<boolean>(false);

  // Storage data
  const [watchedIds, setWatchedIds] = useState<string[]>([]);
  const [customVideos, setCustomVideos] = useState<TacticsVideo[]>([]);
  const [videoOverrides, setVideoOverrides] = useState<Record<string, Partial<TacticsVideo>>>(() => storageService.loadVideoOverrides());

  const stagePlayerRef = useRef<HTMLDivElement>(null);
  const videoElemRef = useRef<HTMLVideoElement>(null);

  const refreshWatched = () => setWatchedIds(storageService.loadWatchedVideos());
  const refreshCustom = () => setCustomVideos(storageService.loadCustomVideos());
  const refreshOverrides = () => setVideoOverrides(storageService.loadVideoOverrides());

  useEffect(() => {
    refreshWatched();
    refreshCustom();
    refreshOverrides();
  }, []);

  useEffect(() => {
    if (initialLevel) {
      setLevelFilter(initialLevel);
    }
  }, [initialLevel]);

  // Combined videos
  const allVideos = useMemo(() => {
    const merged = TACTICS_VIDEOS.map(v => {
      const override = videoOverrides[v.id];
      return override ? { ...v, ...override } : v;
    });
    return [...merged, ...customVideos];
  }, [customVideos, videoOverrides]);

  // Filtered list
  const filteredVideos = useMemo(() => {
    return allVideos.filter(v => {
      // Group filter
      if (activeGroup === 'CORNERS') {
        if (activeCorner !== 'ALL') {
          if (v.category !== activeCorner) return false;
        } else {
          if (!v.category.startsWith('POS_')) return false;
        }
      } else if (activeGroup === 'MATCHES') {
        if (activeMatch !== 'ALL') {
          if (v.category !== activeMatch) return false;
        } else {
          const matchCats = ['DON_NAM', 'DOI_NAM', 'DON_NU', 'DOI_NU'];
          if (!matchCats.includes(v.category)) return false;
        }
      } else if (activeGroup !== 'ALL') {
        if (v.category !== activeGroup) return false;
      }

      // Level filter
      if (levelFilter !== 'ALL' && v.level !== levelFilter) {
        return false;
      }

      // Search filter
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase().trim();
        const matchTitle = v.title.toLowerCase().includes(q);
        const matchSub = v.subTitle?.toLowerCase().includes(q) || false;
        const matchDesc = v.description?.toLowerCase().includes(q) || false;
        const matchTag = v.tags?.some(t => t.toLowerCase().includes(q)) || false;
        if (!matchTitle && !matchSub && !matchDesc && !matchTag) return false;
      }

      return true;
    });
  }, [allVideos, activeGroup, activeCorner, activeMatch, levelFilter, searchQuery]);

  // Handle video selection: set featured player and smoothly scroll to it
  const handleSelectVideo = (v: TacticsVideo, scrollToStage = true) => {
    setCurrentVideo(v);
    setIsPlayingStage(true);
    if (scrollToStage && stagePlayerRef.current) {
      stagePlayerRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  };

  // Auto-next or Next/Prev navigation
  const currentIndex = filteredVideos.findIndex(v => v.id === currentVideo.id);
  const handlePrevVideo = () => {
    if (filteredVideos.length === 0) return;
    const prevIdx = currentIndex > 0 ? currentIndex - 1 : filteredVideos.length - 1;
    handleSelectVideo(filteredVideos[prevIdx], false);
  };

  const handleNextVideo = () => {
    if (filteredVideos.length === 0) return;
    const nextIdx = currentIndex < filteredVideos.length - 1 ? currentIndex + 1 : 0;
    handleSelectVideo(filteredVideos[nextIdx], false);
  };

  const handleStageVideoEnded = () => {
    // Mark completed
    if (!watchedIds.includes(currentVideo.id)) {
      storageService.markVideoWatched(currentVideo.id);
      refreshWatched();
    }
    // Auto advance if enabled
    if (isAutoNext && filteredVideos.length > 1) {
      handleNextVideo();
    }
  };

  const handleToggleWatched = (id: string, e?: React.MouseEvent) => {
    e?.stopPropagation();
    storageService.toggleVideoWatched(id);
    refreshWatched();
  };

  // Thumbnail helper
  const getThumbnailSrc = (video: TacticsVideo): string => {
    if (video.thumbnailUrl) {
      if (video.thumbnailUrl.startsWith('./thumbnails/')) {
        return `${import.meta.env.BASE_URL}thumbnails/${video.thumbnailUrl.replace('./thumbnails/', '')}`;
      }
      return video.thumbnailUrl;
    }
    const ytId = extractYouTubeId(video.videoUrl);
    if (ytId) {
      return `https://img.youtube.com/vi/${ytId}/hqdefault.jpg`;
    }
    return `${import.meta.env.BASE_URL}thumbnails/${video.id}.jpg`;
  };

  // Current active embed info
  const stageYtId = extractYouTubeId(currentVideo.videoUrl);
  const stageTikTokId = extractTikTokId(currentVideo.videoUrl);
  const stageIsTikTok = isTikTokUrl(currentVideo.videoUrl);
  const isCurrentWatched = watchedIds.includes(currentVideo.id);

  const completedCount = allVideos.filter(v => watchedIds.includes(v.id)).length;
  const percentCompleted = allVideos.length > 0 ? Math.round((completedCount / allVideos.length) * 100) : 0;

  return (
    <section className="video-section-container kid-friendly-cinema" ref={stagePlayerRef}>
      {/* Top Banner with Friendly Greeting */}
      <div className="cinema-header-bar">
        <div className="cinema-header-left">
          <div className="cinema-eyebrow">
            <span className="cinema-pulse-dot" />
            <Sparkles size={16} className="text-amber animate-spin-slow" />
            <span>RẠP CHIẾU VIDEO CẦU LÔNG • XEM LÀ BIẾT ĐÁNH</span>
          </div>
          <h2 className="cinema-main-title">
            KHO {allVideos.length} VIDEO KỸ THUẬT & ĐỘNG TÁC CHUẨN
          </h2>
          <p className="cinema-tagline">
            Bấm vào bất kỳ bài nào bên dưới để xem ngay trên màn hình lớn. Tự động chuyển bài học tiếp theo!
          </p>
        </div>

        <div className="cinema-progress-badge">
          <div className="cinema-badge-icon">
            <Star size={24} className="text-amber" fill="currentColor" />
          </div>
          <div className="cinema-badge-info">
            <span className="badge-val">Bé đã học {completedCount}/{allVideos.length} bài</span>
            <div className="badge-bar-track">
              <div className="badge-bar-fill" style={{ width: `${percentCompleted}%` }} />
            </div>
          </div>
        </div>
      </div>

      {/* ============================================================ */}
      {/* 1. FEATURED INLINE STAGE - PHÁT VIDEO TRỰC TIẾP TRÊN MÀN HÌNH */}
      {/* ============================================================ */}
      <div className="featured-stage-card animate-scale-up">
        <div className="stage-screen-wrapper">
          {stageYtId ? (
            <iframe
              key={currentVideo.id}
              src={`https://www.youtube-nocookie.com/embed/${stageYtId}?autoplay=1&rel=0&modestbranding=1`}
              title={currentVideo.title}
              className="stage-embed-frame"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          ) : (stageTikTokId || stageIsTikTok) ? (
            <iframe
              key={currentVideo.id}
              src={stageTikTokId ? `https://www.tiktok.com/embed/v2/${stageTikTokId}` : `https://www.tiktok.com/embed/v2/?url=${encodeURIComponent(currentVideo.videoUrl)}`}
              title={currentVideo.title}
              className="stage-embed-frame"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          ) : (
            <video
              ref={videoElemRef}
              key={currentVideo.id}
              src={currentVideo.videoUrl}
              className="stage-native-video"
              controls
              playsInline
              autoPlay
              onEnded={handleStageVideoEnded}
            />
          )}
        </div>

        {/* Stage Bottom Controller Bar */}
        <div className="stage-control-bar">
          <div className="stage-video-details">
            <div className="stage-badges-row">
              <span className={`stage-level-badge lvl-${currentVideo.level || 'Cơ bản'}`}>
                {currentVideo.level === 'Cơ bản' && '⭐ Dễ (Bé mới học)'}
                {currentVideo.level === 'Trung cấp' && '⚡ Vừa (Đã biết chơi)'}
                {currentVideo.level === 'Nâng cao' && '🔥 Siêu đẳng (Tuyệt chiêu)'}
              </span>
              <span className="stage-category-pill">{currentVideo.subTitle}</span>
            </div>
            <h3 className="stage-video-title">{currentVideo.title}</h3>
            {currentVideo.description && (
              <p className="stage-coaching-tip">💡 <strong>Mẹo của thầy:</strong> {currentVideo.description}</p>
            )}
          </div>

          <div className="stage-action-buttons">
            {/* Auto Next Toggle */}
            <button 
              className={`btn-stage-toggle-autonext ${isAutoNext ? 'active' : ''}`}
              onClick={() => setIsAutoNext(!isAutoNext)}
              title="Tự động phát bài tiếp theo sau khi hết video"
            >
              <RefreshCw size={16} className={isAutoNext ? 'animate-spin-slow' : ''} />
              <span>{isAutoNext ? 'Tự chuyển bài: BẬT' : 'Tự chuyển bài: TẮT'}</span>
            </button>

            {/* Prev / Next */}
            <div className="stage-nav-btn-group">
              <button className="btn-stage-nav" onClick={handlePrevVideo} title="Bài học trước">
                <ChevronLeft size={20} />
                <span>Trước</span>
              </button>
              <button className="btn-stage-nav" onClick={handleNextVideo} title="Bài học tiếp theo">
                <span>Tiếp</span>
                <ChevronRight size={20} />
              </button>
            </div>

            {/* Mark Watched Button */}
            <button 
              className={`btn-stage-watched ${isCurrentWatched ? 'is-done' : ''}`}
              onClick={() => handleToggleWatched(currentVideo.id)}
            >
              <CheckCircle2 size={18} />
              <span>{isCurrentWatched ? 'Đã học xong ⭐' : 'Đánh dấu đã học'}</span>
            </button>

            {/* Fullscreen Theater Modal */}
            <button 
              className="btn-stage-fullscreen"
              onClick={() => setTheaterModalVideo(currentVideo)}
              title="Mở rạp chiếu toàn màn hình"
            >
              <Maximize2 size={18} />
            </button>
          </div>
        </div>
      </div>

      {/* ============================================================ */}
      {/* 2. CHỌN CHUYÊN ĐỀ ĐƠN GIẢN (BIG CATEGORY TABS CHO LỚP 1) */}
      {/* ============================================================ */}
      <div className="kid-category-tabs-strip">
        <div className="kid-tabs-scrollable">
          {CATEGORY_TABS.map(tab => {
            let count = 0;
            if (tab.key === 'ALL') count = allVideos.length;
            else if (tab.key === 'CORNERS') count = allVideos.filter(v => v.category.startsWith('POS_')).length;
            else if (tab.key === 'MATCHES') count = allVideos.filter(v => ['DON_NAM', 'DOI_NAM', 'DON_NU', 'DOI_NU'].includes(v.category)).length;
            else count = allVideos.filter(v => v.category === tab.key).length;

            const isSelected = activeGroup === tab.key;
            return (
              <button
                key={tab.key}
                className={`btn-kid-tab ${isSelected ? 'is-active' : ''}`}
                onClick={() => {
                  setActiveGroup(tab.key);
                  if (tab.key === 'CORNERS') setActiveCorner('ALL');
                  if (tab.key === 'MATCHES') setActiveMatch('ALL');
                }}
              >
                <span className="kid-tab-icon">{tab.icon}</span>
                <span className="kid-tab-name">{tab.label}</span>
                <span className="kid-tab-count">({count})</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Sub-pills for 9 Positions or Match types when selected */}
      {activeGroup === 'CORNERS' && (
        <div className="kid-subpills-row animate-fade-in">
          <button 
            className={`btn-subpill ${activeCorner === 'ALL' ? 'active' : ''}`}
            onClick={() => setActiveCorner('ALL')}
          >
            Tất cả 9 Ô (90)
          </button>
          {CORNER_PILLS.map(p => (
            <button
              key={p.key}
              className={`btn-subpill ${activeCorner === p.key ? 'active' : ''}`}
              onClick={() => setActiveCorner(p.key)}
            >
              <span className="pill-num">{p.num}</span>
              <span>{p.label}</span>
            </button>
          ))}
        </div>
      )}

      {activeGroup === 'MATCHES' && (
        <div className="kid-subpills-row animate-fade-in">
          <button 
            className={`btn-subpill ${activeMatch === 'ALL' ? 'active' : ''}`}
            onClick={() => setActiveMatch('ALL')}
          >
            Tất cả thi đấu (40)
          </button>
          {MATCH_PILLS.map(m => (
            <button
              key={m.key}
              className={`btn-subpill ${activeMatch === m.key ? 'active' : ''}`}
              onClick={() => setActiveMatch(m.key)}
            >
              {m.label}
            </button>
          ))}
        </div>
      )}

      {/* Filters & Search Toolbar (Đơn giản, ít nút, dễ bấm) */}
      <div className="kid-filters-toolbar">
        {/* Simple Difficulty Levels */}
        <div className="kid-level-pills">
          <span className="filter-hint-lbl">Độ khó:</span>
          {(['ALL', 'Cơ bản', 'Trung cấp', 'Nâng cao'] as const).map(lvl => (
            <button
              key={lvl}
              className={`btn-kid-lvl-pill ${levelFilter === lvl ? 'active' : ''} ${lvl !== 'ALL' ? `lvl-${lvl}` : ''}`}
              onClick={() => setLevelFilter(lvl)}
            >
              {lvl === 'ALL' && '⭐ Tất cả'}
              {lvl === 'Cơ bản' && '🌟 Dễ tập'}
              {lvl === 'Trung cấp' && '⚡ Vừa sức'}
              {lvl === 'Nâng cao' && '🔥 Siêu đẳng'}
            </button>
          ))}
        </div>

        {/* Cute Search Input */}
        <div className="kid-search-wrap">
          <Search size={18} className="kid-search-icon" />
          <input
            type="text"
            placeholder="🔍 Bé muốn tìm đập cầu, ve, bộ pháp..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="kid-search-input"
          />
          {searchQuery && (
            <button className="kid-search-clear" onClick={() => setSearchQuery('')}>×</button>
          )}
        </div>
      </div>

      {/* Video Cards Grid */}
      <div className="kid-video-grid">
        {filteredVideos.length === 0 ? (
          <div className="kid-empty-state">
            <Tv size={48} className="empty-icon text-cyan animate-bounce-soft" />
            <h3>Chưa tìm thấy bài tập nào</h3>
            <p>Bé hãy bấm vào nút xem "Tất cả video" nhé!</p>
            <button 
              className="btn-kid-reset"
              onClick={() => {
                setActiveGroup('ALL');
                setLevelFilter('ALL');
                setSearchQuery('');
              }}
            >
              Xem toàn bộ {allVideos.length} bài học 🏸
            </button>
          </div>
        ) : (
          filteredVideos.map((v) => {
            const isSelected = v.id === currentVideo.id;
            const isDone = watchedIds.includes(v.id);
            return (
              <div 
                key={v.id}
                className={`kid-video-card ${isSelected ? 'is-currently-playing' : ''} ${isDone ? 'is-completed' : ''}`}
                onClick={() => handleSelectVideo(v, true)}
                role="button"
                tabIndex={0}
              >
                <div className="kid-thumb-wrap">
                  <img 
                    src={getThumbnailSrc(v)} 
                    alt={v.title} 
                    className="kid-thumb-img"
                    loading="lazy"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = `${import.meta.env.BASE_URL}thumbnails/default.jpg`;
                    }}
                  />
                  <div className="kid-play-overlay">
                    <div className="kid-play-circle">
                      <Play size={20} fill="currentColor" />
                    </div>
                  </div>

                  {/* Badges on Thumbnail */}
                  <div className="kid-thumb-badge-top">
                    <span className={`kid-lvl-tag lvl-${v.level || 'Cơ bản'}`}>
                      {v.level || 'Cơ bản'}
                    </span>
                  </div>

                  {isDone && (
                    <div className="kid-done-badge" title="Bé đã học xong bài này">
                      <CheckCircle2 size={16} fill="#10b981" color="#ffffff" />
                      <span>Đã học</span>
                    </div>
                  )}

                  {isSelected && (
                    <div className="kid-playing-badge">
                      <span className="playing-pulse-dot" />
                      <span>Đang phát</span>
                    </div>
                  )}
                </div>

                <div className="kid-card-body">
                  <h4 className="kid-card-title">{v.title}</h4>
                  <p className="kid-card-subtitle">{v.subTitle}</p>
                  
                  <div className="kid-card-footer">
                    <span className="kid-watch-btn-text">
                      <Play size={14} fill="currentColor" /> Bấm xem ngay
                    </span>
                    <button 
                      className={`kid-toggle-star ${isDone ? 'active' : ''}`}
                      onClick={(e) => handleToggleWatched(v.id, e)}
                      title={isDone ? "Bỏ đánh dấu" : "Đánh dấu đã học"}
                    >
                      <Star size={16} fill={isDone ? "#fbbf24" : "none"} color={isDone ? "#fbbf24" : "#94a3b8"} />
                    </button>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Optional Coach / Admin Accordion (Tucked away so kids are not confused) */}
      <div className="coach-settings-accordion">
        <button 
          className="btn-coach-toggle" 
          onClick={() => setShowAdminTools(!showAdminTools)}
        >
          <Settings size={16} />
          <span>{showAdminTools ? '▲ Ẩn công cụ dành cho Huấn luyện viên' : '⚙️ Tùy chỉnh nâng cao (Dành cho HLV & Phụ huynh)'}</span>
        </button>

        {showAdminTools && (
          <div className="coach-tools-panel animate-fade-in">
            <p className="coach-tools-desc">
              Khu vực dành cho HLV: Gắn link YouTube mới, nhập xuất file JSON hoặc xem hướng dẫn video unlisted.
            </p>
            <div className="coach-buttons-row">
              <button 
                className="btn-coach-item"
                onClick={() => setIsGuideModalOpen(true)}
              >
                <Youtube size={16} className="text-danger" />
                <span>Hướng dẫn YouTube Unlisted</span>
              </button>
              <button 
                className="btn-coach-item"
                onClick={() => setIsBatchModalOpen(true)}
              >
                <span>Nhập / Xuất JSON</span>
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Theater Modal for Fullscreen View */}
      {theaterModalVideo && (
        <VideoPlayerModal
          video={theaterModalVideo}
          isOpen={true}
          onClose={() => setTheaterModalVideo(null)}
          onWatchedChanged={refreshWatched}
        />
      )}

      {/* Coach Modals */}
      <YouTubeGuideModal
        isOpen={isGuideModalOpen}
        onClose={() => setIsGuideModalOpen(false)}
      />

      <BatchImportExportModal
        isOpen={isBatchModalOpen}
        onClose={() => setIsBatchModalOpen(false)}
        onDataChanged={() => {
          refreshCustom();
          refreshOverrides();
        }}
      />
    </section>
  );
};
