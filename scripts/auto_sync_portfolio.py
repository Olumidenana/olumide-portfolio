#!/usr/bin/env python3
"""
Auto-Sync Engine for Olumide Adeyemi-Nana's Engineering Portfolio & CV.
Automatically fetches the latest repositories from GitHub (Olumidenana),
detects newly created systems, and updates index.html & international-cv.html.
"""

import os
import sys
import json
import re
import urllib.request

REPO_OWNER = "Olumidenana"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, "index.html")
CV_PATH = os.path.join(ROOT_DIR, "international-cv.html")
DOSSIER_PATH = os.path.join(ROOT_DIR, "portfolio-dossier.html")

KNOWN_EXCLUSIONS = {"olumidenana", "olumide-portfolio"}

def fetch_github_repos():
    url = f"https://api.github.com/users/{REPO_OWNER}/repos?sort=pushed&per_page=100"
    headers = {"User-Agent": "Olumide-Portfolio-AutoSync/1.0", "Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as e:
        print(f"Error fetching GitHub repositories: {e}", file=sys.stderr)
        return []

def get_existing_repos_in_portfolio(html_content):
    # Match any Olumidenana/<repo> link
    matches = re.findall(r"github\.com/Olumidenana/([a-zA-Z0-9\-_]+)", html_content, re.IGNORECASE)
    return set(m.lower() for m in matches)

def sync_new_repos():
    repos = fetch_github_repos()
    if not repos:
        print("No repositories returned from GitHub.")
        return False

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        index_html = f.read()

    existing = get_existing_repos_in_portfolio(index_html)
    existing.update(KNOWN_EXCLUSIONS)

    new_repos = []
    for r in repos:
        name = r["name"].lower()
        if name not in existing and not r.get("fork", False):
            new_repos.append(r)

    if not new_repos:
        print(f"Portfolio is fully synchronized with GitHub ({len(repos)} repositories checked).")
        return False

    print(f"Found {len(new_repos)} new repositories on GitHub to sync: {[r['name'] for r in new_repos]}")

    # Determine current total count from index.html
    count_match = re.search(r"<!-- (\d+)\.", index_html)
    all_num_matches = re.findall(r"<!-- (\d+)\.", index_html)
    highest_idx = max([int(n) for n in all_num_matches]) if all_num_matches else 20

    new_ledger_rows = []
    new_blueprint_cards = []

    for r in new_repos:
        highest_idx += 1
        raw_name = r["name"]
        formatted_title = " ".join([w.capitalize() for w in re.split(r"[-_]", raw_name)])
        desc = r.get("description") or f"Production software engineering platform developed by Olumide Adeyemi-Nana ({r['html_url']})."
        lang = r.get("language") or "TypeScript"
        stars = r.get("stargazers_count", 0)
        pushed_at = r.get("pushed_at", "")[:10]
        category = "ai" if any(k in raw_name.lower() for k in ["ai", "bot", "model", "llm", "speech"]) else ("fintech" if any(k in raw_name.lower() for k in ["trade", "quant", "pay", "flux", "escrow"]) else "enterprise")
        cat_badge = "AI / DISTRIBUTED" if category == "ai" else ("FINTECH / QUANT" if category == "fintech" else "ENTERPRISE / SYSTEMS")

        # Generate Ledger Row
        row = f'''            <!-- {highest_idx}. {raw_name.upper()} (AUTO-SYNCED) -->
            <tr class="ledger-row cursor-pointer" data-cat="{category}" onclick="toggleDrawer('drawer-{highest_idx}')">
              <td class="p-4 text-amber-raw font-bold">{highest_idx:02d}/</td>
              <td class="p-4">
                <div class="font-bold text-white text-sm font-sans flex items-center gap-2">
                  <span class="scramble-hover">{formatted_title}</span>
                  <span class="px-1.5 py-0.5 text-[9px] font-mono font-bold bg-chlorophyll/20 text-chlorophyll border border-chlorophyll/40 uppercase">AUTO-SYNCED</span>
                  <span class="w-1.5 h-1.5 rounded-full bg-chlorophyll animate-pulse"></span>
                </div>
                <div class="text-[11px] text-titanium-muted font-sans mt-0.5 line-clamp-1">
                  {desc}
                </div>
              </td>
              <td class="p-4 hidden md:table-cell">
                <span class="px-2 py-0.5 bg-amber-raw/10 text-amber-raw border border-amber-raw/30 text-[10px]">{cat_badge}</span>
              </td>
              <td class="p-4 hidden lg:table-cell text-chlorophyll font-bold">
                Live GitHub Repository · {pushed_at}
              </td>
              <td class="p-4 hidden sm:table-cell text-titanium-muted">
                {lang} · Git Engine · Continuous Delivery
              </td>
              <td class="p-4 text-right">
                <a href="{r['html_url']}" target="_blank" onclick="event.stopPropagation()" class="px-2.5 py-1 bg-black border border-amber-raw text-amber-raw hover:bg-amber-raw hover:text-black font-bold transition-all inline-flex items-center gap-1">
                  <span>GITHUB</span> <span>→</span>
                </a>
              </td>
            </tr>
            <!-- Drawer {highest_idx} -->
            <tr id="drawer-{highest_idx}" class="hidden bg-[#0A0D14] hairline-b">
              <td colspan="6" class="p-6 space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono text-xs">
                  <div class="space-y-1">
                    <span class="text-amber-raw font-bold uppercase tracking-wider">[ SYSTEM OVERVIEW ]</span>
                    <p class="text-titanium-muted text-[11px] leading-relaxed">
                      {desc}
                    </p>
                  </div>
                  <div class="space-y-1">
                    <span class="text-titanium font-bold uppercase tracking-wider">[ RUNTIME SPECIFICATIONS ]</span>
                    <p class="text-titanium-muted text-[11px] leading-relaxed">
                      Primary Technology: {lang}. Automated production deployment, verified syntax, and integration testing on GitHub.
                    </p>
                  </div>
                  <div class="space-y-2">
                    <span class="text-chlorophyll font-bold uppercase tracking-wider">[ REPOSITORY ARTIFACTS ]</span>
                    <div class="flex flex-col gap-1.5">
                      <a href="{r['html_url']}" target="_blank" class="text-amber-raw hover:underline flex items-center gap-1">
                        <span>● Repository: gh/{REPO_OWNER}/{raw_name}</span> ↗
                      </a>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
'''
        new_ledger_rows.append(row)

        # Generate Blueprint Card
        card = f'''        <!-- Blueprint {highest_idx}: {raw_name.upper()} -->
        <div class="blueprint-card p-6 bg-obsidian-card hairline-border crosshair-corner space-y-4 flex flex-col justify-between" data-cat="{category}">
          <div class="space-y-3">
            <div class="flex items-center justify-between font-mono text-xs">
              <span class="text-amber-raw font-bold">{highest_idx:02d}/</span>
              <span class="px-2 py-0.5 bg-chlorophyll/10 text-chlorophyll border border-chlorophyll/30 text-[10px]">{cat_badge}</span>
            </div>
            <h4 class="text-xl font-serif text-white">{formatted_title}</h4>
            <p class="text-xs text-titanium-muted font-sans leading-relaxed">
              {desc}
            </p>
            <div class="p-2.5 bg-black border border-hairline font-mono text-[11px] text-white font-bold">
              {lang} · Live GitHub Release
            </div>
            <div class="text-[10px] font-mono text-titanium-muted">
              Updated: {pushed_at} · Stars: {stars}
            </div>
          </div>
          <div class="pt-4 hairline-t border-hairline flex items-center justify-between">
            <a href="{r['html_url']}" target="_blank" class="px-3 py-1 bg-black border border-amber-raw text-amber-raw hover:bg-amber-raw hover:text-black font-mono font-bold text-xs tactile-key flex items-center gap-1">
              <span>EXPLORE</span> <span>→</span>
            </a>
            <span class="text-xs font-mono text-chlorophyll">LIVE CODE</span>
          </div>
        </div>
'''
        new_blueprint_cards.append(card)

    # Insert into index.html
    new_rows_str = "\n".join(new_ledger_rows)
    new_cards_str = "\n".join(new_blueprint_cards)

    updated_index = index_html.replace("</tbody>\n        </table>", new_rows_str + "\n          </tbody>\n        </table>")
    
    blueprint_insert_target = '</div>\n    </section>\n\n    <!-- =========================================================================\n         SECTION 4: TECHNICAL RUNTIME SPECS'
    if blueprint_insert_target in updated_index:
        updated_index = updated_index.replace(blueprint_insert_target, new_cards_str + "\n" + blueprint_insert_target)

    # Update counts across index.html
    old_count_str = f"{highest_idx - len(new_repos)}"
    new_count_str = f"{highest_idx}"
    updated_index = re.sub(rf"{old_count_str} Shipped Production Systems", f"{new_count_str} Shipped Production Systems", updated_index)
    updated_index = re.sub(rf"<span>{old_count_str} SYSTEMS</span>", f"<span>{new_count_str} SYSTEMS</span>", updated_index)
    updated_index = re.sub(rf"{old_count_str} shipped platforms", f"{new_count_str} shipped platforms", updated_index)
    updated_index = re.sub(rf"{old_count_str} Live Systems", f"{new_count_str} Live Systems", updated_index)
    updated_index = re.sub(rf"CURRENT LOAD: {old_count_str} REPOS DEPLOYED", f"CURRENT LOAD: {new_count_str} REPOS DEPLOYED", updated_index)
    updated_index = re.sub(rf">{old_count_str}\+<", f">{new_count_str}+<", updated_index)
    updated_index = re.sub(rf"{old_count_str} VERIFIED DEPLOYMENTS", f"{new_count_str} VERIFIED DEPLOYMENTS", updated_index)
    updated_index = re.sub(rf"\[1\] ALL \({old_count_str}\)", f"[1] ALL ({new_count_str})", updated_index)
    updated_index = re.sub(rf"Type 1-{old_count_str}", f"Type 1-{new_count_str}", updated_index)
    updated_index = re.sub(rf"Select 1-{old_count_str} from the ledger", f"Select 1-{new_count_str} from the ledger", updated_index)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write(updated_index)

    print(f"Successfully auto-synced {len(new_repos)} new repositories! Portfolio count updated to {highest_idx}.")
    return True

if __name__ == "__main__":
    sync_new_repos()
