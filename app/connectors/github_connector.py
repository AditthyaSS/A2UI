"""GitHub Data Connector - Real-time GitHub API integration."""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict
import time

try:
    from github import Github, GithubException
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False


@dataclass
class GitHubUserData:
    """GitHub user data model."""
    username: str
    total_commits: int
    repo_count: int
    top_language: str
    commit_history: List[Dict[str, Any]]
    language_distribution: List[Dict[str, Any]]
    top_repositories: List[Dict[str, Any]]


class GitHubConnector:
    """GitHub API connector with caching and error handling."""
    
    def __init__(self, token: Optional[str] = None, cache_ttl: int = 300):
        """Initialize GitHub connector.
        
        Args:
            token: GitHub personal access token (optional)
            cache_ttl: Cache time-to-live in seconds
        """
        if not GITHUB_AVAILABLE:
            raise ImportError("PyGithub not installed. Run: pip install PyGithub")
        
        self.github = Github(token) if token else Github()
        self.cache: Dict[str, tuple[GitHubUserData, float]] = {}
        self.cache_ttl = cache_ttl
    
    def get_user_data(self, username: str) -> GitHubUserData:
        """Fetch comprehensive user data from GitHub.
        
        Args:
            username: GitHub username
            
        Returns:
            GitHubUserData with all metrics
            
        Raises:
            GithubException: If user not found or API error
        """
        # Check cache
        if username in self.cache:
            data, timestamp = self.cache[username]
            if time.time() - timestamp < self.cache_ttl:
                return data
        
        # Fetch fresh data
        try:
            user = self.github.get_user(username)
            repos = list(user.get_repos())
            
            # Calculate metrics
            total_commits = self._count_user_commits(user, repos)
            repo_count = len([r for r in repos if not r.fork])
            top_language = self._get_top_language(repos)
            commit_history = self._get_commit_history(user, repos)
            language_distribution = self._get_language_distribution(repos)
            top_repositories = self._get_top_repositories(repos)
            
            # Create data object
            data = GitHubUserData(
                username=username,
                total_commits=total_commits,
                repo_count=repo_count,
                top_language=top_language,
                commit_history=commit_history,
                language_distribution=language_distribution,
                top_repositories=top_repositories
            )
            
            # Cache it
            self.cache[username] = (data, time.time())
            
            return data
            
        except GithubException as e:
            raise Exception(f"GitHub API error: {e.status} - {e.data.get('message', 'Unknown error')}")
    
    def _count_user_commits(self, user, repos: List) -> int:
        """Count total commits by user across all repos.
        
        Args:
            user: GitHub user object
            repos: List of repositories
            
        Returns:
            Total commit count
        """
        total = 0
        # Sample recent commits from user's repos
        for repo in repos[:10]:  # Limit to avoid rate limiting
            try:
                commits = repo.get_commits(author=user, since=datetime.now() - timedelta(days=365))
                total += commits.totalCount
            except:
                continue
        return total
    
    def _get_top_language(self, repos: List) -> str:
        """Get user's most used language.
        
        Args:
            repos: List of repositories
            
        Returns:
            Top language name
        """
        language_counts = defaultdict(int)
        
        for repo in repos:
            if repo.language:
                language_counts[repo.language] += 1
        
        if not language_counts:
            return "Unknown"
        
        return max(language_counts.items(), key=lambda x: x[1])[0]
    
    def _get_commit_history(self, user, repos: List, months: int = 6) -> List[Dict[str, Any]]:
        """Get commit activity over time.
        
        Args:
            user: GitHub user object
            repos: List of repositories
            months: Number of months to analyze
            
        Returns:
            List of {date, commits} dictionaries
        """
        # Group commits by month
        monthly_commits = defaultdict(int)
        cutoff_date = datetime.now() - timedelta(days=months * 30)
        
        for repo in repos[:10]:  # Limit to avoid rate limiting
            try:
                commits = repo.get_commits(author=user, since=cutoff_date)
                for commit in commits:
                    month = commit.commit.author.date.strftime("%Y-%m")
                    monthly_commits[month] += 1
            except:
                continue
        
        # Convert to sorted list
        result = []
        for i in range(months):
            date = (datetime.now() - timedelta(days=i * 30)).strftime("%Y-%m")
            result.append({
                "date": date,
                "commits": monthly_commits.get(date, 0)
            })
        
        return sorted(result, key=lambda x: x["date"])
    
    def _get_language_distribution(self, repos: List) -> List[Dict[str, Any]]:
        """Get distribution of languages used.
        
        Args:
            repos: List of repositories
            
        Returns:
            List of {language, percentage} dictionaries
        """
        language_counts = defaultdict(int)
        
        for repo in repos:
            if repo.language:
                language_counts[repo.language] += 1
        
        if not language_counts:
            return []
        
        total = sum(language_counts.values())
        
        result = [
            {
                "language": lang,
                "percentage": round((count / total) * 100)
            }
            for lang, count in language_counts.items()
        ]
        
        return sorted(result, key=lambda x: x["percentage"], reverse=True)[:5]
    
    def _get_top_repositories(self, repos: List, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top repositories by stars.
        
        Args:
            repos: List of repositories
            limit: Number of repos to return
            
        Returns:
            List of {name, stars, commits} dictionaries
        """
        # Filter out forks and sort by stars
        non_fork_repos = [r for r in repos if not r.fork]
        sorted_repos = sorted(non_fork_repos, key=lambda r: r.stargazers_count, reverse=True)
        
        result = []
        for repo in sorted_repos[:limit]:
            result.append({
                "name": repo.name,
                "stars": repo.stargazers_count,
                "commits": repo.get_commits().totalCount if repo.get_commits().totalCount < 1000 else "1000+"
            })
        
        return result
