"""
Advanced Analytics Module for GhostLAN SimWorld
Provides advanced analytics and machine learning capabilities
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class AdvancedAnalytics:
    """Advanced analytics and ML capabilities for GhostLAN"""
    
    def __init__(self, db_path: str = "analytics.db"):
        """Initialize advanced analytics"""
        self.db_path = db_path
        self.models = {}
        self.analytics_cache = {}
        logger.info("Advanced Analytics initialized")
    
    def analyze_player_performance(self, player_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze player performance patterns"""
        if not player_data:
            return {}
        
        df = pd.DataFrame(player_data)
        
        # Safe column access with None checks
        result_col = df.get("result", pd.Series(["loss"] * len(df)))
        kills_col = df.get("kills", pd.Series([0] * len(df)))
        deaths_col = df.get("deaths", pd.Series([0] * len(df)))
        assists_col = df.get("assists", pd.Series([0] * len(df)))
        accuracy_col = df.get("accuracy", pd.Series([0] * len(df)))
        headshot_col = df.get("headshot_ratio", pd.Series([0] * len(df)))
        performance_col = df.get("performance_score", pd.Series([0] * len(df)))
        
        analysis = {
            "total_matches": len(df),
            "win_rate": (result_col == "win").mean() if result_col is not None else 0,
            "avg_kills": kills_col.mean() if kills_col is not None else 0,
            "avg_deaths": deaths_col.mean() if deaths_col is not None else 0,
            "avg_assists": assists_col.mean() if assists_col is not None else 0,
            "accuracy": accuracy_col.mean() if accuracy_col is not None else 0,
            "headshot_ratio": headshot_col.mean() if headshot_col is not None else 0,
            "performance_trend": self._calculate_trend(performance_col),
            "consistency_score": self._calculate_consistency(df),
            "improvement_rate": self._calculate_improvement_rate(df)
        }
        
        return analysis
    
    def detect_anomalies(self, data: List[Dict[str, Any]], threshold: float = 2.0) -> List[Dict[str, Any]]:
        """Detect statistical anomalies in player data"""
        if not data:
            return []
        
        df = pd.DataFrame(data)
        anomalies = []
        
        # Calculate z-scores for numerical columns
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numerical_cols:
            if col in df.columns and len(df[col].dropna()) > 0:
                series = df[col]
                if series is not None and len(series) > 0:
                    mean_val = series.mean()
                    std_val = series.std()
                    if std_val > 0:
                        z_scores = np.abs((series - mean_val) / std_val)
                        anomaly_indices = z_scores > threshold
                        
                        for idx in df[anomaly_indices].index:
                            anomalies.append({
                                "index": idx,
                                "column": col,
                                "value": df.loc[idx, col],
                                "z_score": z_scores[idx],
                                "timestamp": data[idx].get("timestamp", None)
                            })
        
        return anomalies
    
    def predict_match_outcome(self, match_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict match outcome based on historical data"""
        # Simple heuristic-based prediction
        # In production, this would use a trained ML model
        
        team_a_strength = self._calculate_team_strength(match_data.get("team_a", []))
        team_b_strength = self._calculate_team_strength(match_data.get("team_b", []))
        
        total_strength = team_a_strength + team_b_strength
        if total_strength == 0:
            return {"team_a_win_probability": 0.5, "team_b_win_probability": 0.5}
        
        team_a_prob = team_a_strength / total_strength
        team_b_prob = team_b_strength / total_strength
        
        return {
            "team_a_win_probability": team_a_prob,
            "team_b_win_probability": team_b_prob,
            "confidence": min(team_a_prob, team_b_prob) * 2  # Higher confidence when teams are more balanced
        }
    
    def generate_heatmap_data(self, match_events: List[Dict[str, Any]], map_size: Tuple[int, int] = (100, 100)) -> Dict[str, Any]:
        """Generate heatmap data from match events"""
        if not match_events:
            return {"heatmap": np.zeros(map_size).tolist()}
        
        heatmap = np.zeros(map_size)
        
        for event in match_events:
            location = event.get("location")
            if location and len(location) >= 2:
                x, y = int(location[0] * map_size[0]), int(location[1] * map_size[1])
                if 0 <= x < map_size[0] and 0 <= y < map_size[1]:
                    heatmap[x, y] += 1
        
        return {
            "heatmap": heatmap.tolist(),
            "max_intensity": float(heatmap.max()),
            "total_events": len(match_events)
        }
    
    def analyze_team_dynamics(self, team_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze team dynamics and coordination"""
        if not team_data:
            return {}
        
        df = pd.DataFrame(team_data)
        
        # Safe column access
        communication_col = df.get("communication_count", pd.Series([0] * len(df)))
        
        analysis = {
            "team_size": len(df),
            "avg_communication_frequency": communication_col.mean() if communication_col is not None else 0,
            "coordination_score": self._calculate_coordination_score(df),
            "role_distribution": self._analyze_role_distribution(df),
            "team_synergy": self._calculate_team_synergy(df)
        }
        
        return analysis
    
    def _calculate_trend(self, series: Optional[pd.Series]) -> str:
        """Calculate trend direction"""
        if series is None or len(series) < 2:
            return "stable"
        
        slope = np.polyfit(range(len(series)), series, 1)[0]
        
        if slope > 0.1:
            return "improving"
        elif slope < -0.1:
            return "declining"
        else:
            return "stable"
    
    def _calculate_consistency(self, df: pd.DataFrame) -> float:
        """Calculate consistency score"""
        if len(df) < 2:
            return 1.0
        
        performance_cols = ["kills", "deaths", "assists", "accuracy"]
        available_cols = [col for col in performance_cols if col in df.columns]
        
        if not available_cols:
            return 1.0
        
        # Calculate coefficient of variation for each metric
        cv_scores = []
        for col in available_cols:
            series = df[col]
            if series is not None and series.std() > 0:
                cv = series.std() / series.mean()
                cv_scores.append(1 / (1 + cv))  # Convert to consistency score
        
        return float(np.mean(cv_scores)) if cv_scores else 1.0
    
    def _calculate_improvement_rate(self, df: pd.DataFrame) -> float:
        """Calculate improvement rate over time"""
        if len(df) < 2:
            return 0.0
        
        # Use performance score or kills as improvement metric
        metric = df.get("performance_score", df.get("kills", pd.Series([0] * len(df))))
        
        if metric is None or len(metric) < 2:
            return 0.0
        
        # Calculate improvement per match
        improvements = np.diff(metric)
        return float(np.mean(improvements)) if len(improvements) > 0 else 0.0
    
    def _calculate_team_strength(self, players: List[Dict[str, Any]]) -> float:
        """Calculate team strength based on player stats"""
        if not players:
            return 0.0
        
        total_strength = 0.0
        for player in players:
            # Weight different stats
            kills = player.get("kills", 0) * 2.0
            assists = player.get("assists", 0) * 1.0
            accuracy = player.get("accuracy", 0.5) * 100
            experience = player.get("experience_level", 1) * 0.5
            
            player_strength = kills + assists + accuracy + experience
            total_strength += player_strength
        
        return total_strength / len(players)
    
    def _calculate_coordination_score(self, df: pd.DataFrame) -> float:
        """Calculate team coordination score"""
        if len(df) < 2:
            return 0.0
        
        # Simple coordination metric based on communication and proximity
        communication_col = df.get("communication_count", pd.Series([0] * len(df)))
        proximity_col = df.get("avg_team_proximity", pd.Series([0] * len(df)))
        
        communication_score = communication_col.mean() / 10.0 if communication_col is not None else 0  # Normalize
        proximity_score = proximity_col.mean() / 100.0 if proximity_col is not None else 0  # Normalize
        
        return min(1.0, (communication_score + proximity_score) / 2)
    
    def _analyze_role_distribution(self, df: pd.DataFrame) -> Dict[str, int]:
        """Analyze role distribution in team"""
        if "role" not in df.columns:
            return {"unknown": len(df)}
        
        role_series = df["role"]
        if role_series is not None:
            return role_series.value_counts().to_dict()
        return {"unknown": len(df)}
    
    def _calculate_team_synergy(self, df: pd.DataFrame) -> float:
        """Calculate team synergy score"""
        if len(df) < 2:
            return 0.0
        
        # Calculate synergy based on complementary skills
        role_series = df.get("role", pd.Series(["unknown"] * len(df)))
        if role_series is not None:
            roles = role_series.value_counts()
            skill_diversity = len(roles) / len(df)  # Higher diversity = better synergy
        else:
            skill_diversity = 0.0
        
        # Consider team performance consistency
        performance_consistency = self._calculate_consistency(df)
        
        return (skill_diversity + performance_consistency) / 2
    
    def export_analytics_report(self, filepath: str, data: Dict[str, Any]) -> bool:
        """Export analytics report to JSON file"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "analytics_version": "1.0.0",
                "data": data
            }
            
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logger.info(f"Analytics report exported to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export analytics report: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources"""
        self.models.clear()
        self.analytics_cache.clear()
        logger.info("Advanced Analytics cleaned up") 