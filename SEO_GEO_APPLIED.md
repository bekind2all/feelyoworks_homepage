# SEO/GEO 작업 기록

- 작업일: 2026-06-26 11:29:43 +09:00
- 원본 폴더: C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage
- 작업 복제본: C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage_seo_geo_20260626-112900
- 원본은 수정하지 않았습니다.

## 변경한 파일

- index.html: head 메타데이터, canonical, OG/Twitter, JSON-LD 추가
- profile.html: 조은이 강사 검색용 head 메타데이터, ProfilePage/Person JSON-LD 추가
- insights.html: 오늘AI 뉴스레터 검색용 head 메타데이터, CollectionPage JSON-LD 추가
- robots.txt: 검색/AI 검색 수집 정책과 sitemap 위치 추가
- sitemap.xml: 주요 canonical URL 등록
- llms.txt: AI 검색용 사이트 요약과 핵심 엔티티 정리
- _headers: X-Robots-Tag, sitemap/robots/llms 콘텐츠 타입 추가
- _redirects: /profile.html, /insights.html canonical redirect 추가
- functions/_middleware.js: www.feelyoworks.com을 feelyoworks.com으로 301 정규화하고 기존 .html 경로를 canonical 경로로 redirect
- google9bc1d9b7c6206944.html: Google Search Console URL 접두어 속성 소유권 확인 파일

## 배포

- Cloudflare Pages 기존 프로젝트: feelyoworks-homepage
- 최종 배포 미리보기: https://8bdd68d8.feelyoworks-homepage.pages.dev
- 실제 도메인: https://feelyoworks.com/
- 배포용 공개 폴더: C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage_seo_geo_20260626-112900_deploy_public

## Google Search Console

- 속성 유형: URL 접두어
- 등록 URL: https://feelyoworks.com/
- 소유권 확인: HTML 파일 방식 완료
- 인증 파일: https://feelyoworks.com/google9bc1d9b7c6206944.html
- sitemap 제출: https://feelyoworks.com/sitemap.xml
- sitemap 상태: 성공
- 발견된 페이지: 3
- 색인 생성 요청 완료:
  - https://feelyoworks.com/
  - https://feelyoworks.com/profile
  - https://feelyoworks.com/insights

## 검증

- index.html, profile.html, insights.html의 body 영역은 원본과 동일하게 유지했습니다.
- 최종 검증 리포트: SEO_GEO_AUDIT_20260626.md
- 2026-06-30 WordPress 최신 글 반영 확인:
  - 최신 RSS 글: AI를 어디에 둘지 먼저 묻는 날
  - live `/data/insights.json` 업데이트: 2026-06-30T03:40:50+00:00
  - 최종 배포 미리보기: https://25bd1f5e.feelyoworks-homepage.pages.dev
- https://feelyoworks.com/ title/canonical/JSON-LD 확인 완료
- https://feelyoworks.com/profile title/canonical/JSON-LD 확인 완료
- https://feelyoworks.com/insights title/canonical/JSON-LD 확인 완료
- https://feelyoworks.com/sitemap.xml 200 OK 확인 완료
- https://feelyoworks.com/robots.txt 200 OK 확인 완료
- https://feelyoworks.com/llms.txt 200 OK 확인 완료
- https://www.feelyoworks.com/ -> https://feelyoworks.com/ 301 redirect 확인 완료
- https://feelyoworks.com/profile.html -> /profile redirect 확인 완료
- https://feelyoworks.com/insights.html -> /insights redirect 확인 완료

## 되돌리기

1. 원본 폴더는 그대로 보존되어 있습니다.
2. 복제본 안의 변경 전 파일은 .seo-backup 폴더에 있습니다.
3. 복제본에서만 되돌릴 때는 .seo-backup의 파일을 루트로 복사하면 됩니다.
4. 배포를 되돌릴 때는 Cloudflare Pages의 이전 배포로 rollback하면 됩니다.
