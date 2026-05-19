# AI Product Radar 每周深度分析 - 执行历史

## 执行记录

### 2026-05-19（首次执行）
- **执行结果**：无符合深度分析条件的产品
- **原因**：数据库中所有 34 个产品均在当天首次入库（firstSeen = 2026-05-19），距今 0 天，未满足"10天以上且近7天仍活跃"的条件
- **已在日报推荐**：3 个产品（We let AIs run radio stations / Running the second public ODoH relay / Browser based sythesizer, drum machine and squencer），但首次发现时间均为当天
- **后续操作**：build_site.py 生成 3 个产品页，deploy.sh 推送到 GitHub Pages
- **GitHub Pages**：https://terranc.github.io/aI-product-daily-peport/
- **关键发现**：GVM 会劫持 `git` 命令（通过 .zshrc），需用 `/opt/homebrew/bin/git -C <dir>` 绕过；Python 脚本需用 `/opt/homebrew/bin/python3 /absolute/path/to/script.py` 而非 `cd && python3 script.py` 方式运行

---
*下次深度分析预计在数据库积累 10 天后（约 2026-05-29）才会有候选产品出现。*
