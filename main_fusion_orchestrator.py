#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Orquestrador Principal da Fusão Claude-Gemini
Local: FUSAO_EXTREMA/main_fusion_orchestrator.py
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

# Importa os componentes criados
from arsenal.intelligence_fusion import IntelligenceFusion, create_fusion_engine
from arsenal.logger_system import get_fusion_logger

class FusionOrchestrator:
    """
    Orquestrador principal para coordenação da fusão Claude-Gemini
    """

    def __init__(self):
        self.fusion_engine = create_fusion_engine()
        self.logger = get_fusion_logger()
        self.model_profiles = self._load_model_profiles()
        self.knowledge_graph = self._load_knowledge_graph()
        self.response_weights = self._load_response_weights()

        self.logger.log_fusion_event("orchestrator_init", {
            "timestamp": "now",
            "components_loaded": 4
        })

    def _load_model_profiles(self) -> Dict[str, Any]:
        """Carrega perfis dos modelos"""
        try:
            with open("entidades/model_profiles.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.log_error("model_profiles.json não encontrado")
            return {}

    def _load_knowledge_graph(self) -> Dict[str, Any]:
        """Carrega grafo de conhecimento"""
        try:
            with open("entidades/knowledge_graph.yaml", 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.log_error("knowledge_graph.yaml não encontrado")
            return {}

    def _load_response_weights(self) -> Dict[str, Any]:
        """Carrega pesos de resposta"""
        try:
            with open("entidades/response_weights.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.log_error("response_weights.json não encontrado")
            return {}

    def determine_task_type(self, prompt: str) -> str:
        """
        Determina automaticamente o tipo de tarefa baseado no prompt
        """
        prompt_lower = prompt.lower()

        technical_keywords = ['program', 'code', 'algorithm', 'technical', 'function', 'debug', 'implement']
        creative_keywords = ['create', 'design', 'innovate', 'brainstorm', 'imagine', 'story', 'art']
        analytical_keywords = ['analyze', 'evaluate', 'compare', 'assess', 'examine', 'review']
        problem_solving_keywords = ['solve', 'resolve', 'fix', 'address', 'tackle', 'overcome']

        scores = {
            'technical': sum(1 for kw in technical_keywords if kw in prompt_lower),
            'creative': sum(1 for kw in creative_keywords if kw in prompt_lower),
            'analytical': sum(1 for kw in analytical_keywords if kw in prompt_lower),
            'problem_solving': sum(1 for kw in problem_solving_keywords if kw in prompt_lower)
        }

        # Retorna o tipo com maior pontuação
        dominant_type = max(scores, key=scores.get)
        confidence = scores[dominant_type] / sum(scores.values()) if sum(scores.values()) > 0 else 0

        self.logger.log_fusion_event("task_classification", {
            "prompt_sample": prompt[:50],
            "classification": dominant_type,
            "confidence": confidence,
            "scores": scores
        })

        return dominant_type if confidence > 0.2 else 'general'

    def optimize_prompt_for_models(self, original_prompt: str, task_type: str) -> Dict[str, str]:
        """
        Otimiza o prompt para cada modelo com base no tipo de tarefa
        """
        # Carrega perfis dos modelos
        claude_profile = self.model_profiles.get('claude_profile', {})
        gemini_profile = self.model_profiles.get('gemini_profile', {})

        # Define estratégias de otimização
        optimizations = {
            'technical': {
                'claude': f"Como especialista técnico, {original_prompt}",
                'gemini': f"Considerando aspectos técnicos e inovações relacionadas a: {original_prompt}"
            },
            'creative': {
                'claude': f"Analise criticamente esta proposta criativa: {original_prompt}",
                'gemini': f"Explore ideias criativas e inovadoras para: {original_prompt}"
            },
            'analytical': {
                'claude': f"Forneça uma análise detalhada e crítica de: {original_prompt}",
                'gemini': f"Analise sob múltiplas perspectivas: {original_prompt}"
            },
            'problem_solving': {
                'claude': f"Sistema e metodicamente resolva: {original_prompt}",
                'gemini': f"Proponha múltiplas abordagens para resolver: {original_prompt}"
            }
        }

        # Retorna prompts otimizados
        task_optimization = optimizations.get(task_type, {
            'claude': original_prompt,
            'gemini': original_prompt
        })

        return task_optimization

    def execute_fusion_process(self, prompt: str) -> Dict[str, Any]:
        """
        Executa o processo completo de fusão Claude-Gemini
        """
        self.logger.log_fusion_event("fusion_start", {
            "prompt": prompt[:100],
            "timestamp": "now"
        })

        # Determina tipo de tarefa
        task_type = self.determine_task_type(prompt)

        # Otimiza prompts para cada modelo
        optimized_prompts = self.optimize_prompt_for_models(prompt, task_type)

        # Simula respostas dos modelos (na prática, você chamaria as APIs reais)
        claude_response = f"[Claude - {task_type}] Resposta simulada para: {optimized_prompts['claude'][:50]}..."
        gemini_response = f"[Gemini - {task_type}] Resposta simulada para: {optimized_prompts['gemini'][:50]}..."

        # Executa fusão
        fusion_result = self.fusion_engine.fuse_responses(
            claude_response,
            gemini_response,
            task_type
        )

        # Registra métricas de performance
        performance_metrics = {
            "task_type": task_type,
            "synergy_score": fusion_result['synergy_score'],
            "processing_time": "simulated",
            "models_used": ["claude", "gemini"]
        }

        self.logger.log_performance_metrics(performance_metrics)

        # Retorna resultado completo
        result = {
            "original_prompt": prompt,
            "task_type": task_type,
            "optimized_prompts": optimized_prompts,
            "fusion_result": fusion_result,
            "performance_metrics": performance_metrics
        }

        self.logger.log_fusion_event("fusion_complete", {
            "result_summary": f"Fusão concluída com score {fusion_result['synergy_score']:.2f}",
            "task_type": task_type
        })

        return result

    def get_advice_for_best_results(self) -> str:
        """
        Retorna conselhos para obter melhores resultados com a fusão
        """
        advice = """
        CONSELHOS PARA MELHORES RESULTADOS COM A FUSÃO CLAUDE-GEMINI:

        1. Especifique claramente o tipo de tarefa (técnica, criativa, analítica, etc.)
        2. Use prompts bem estruturados e específicos
        3. Para tarefas técnicas: Destaque aspectos de programação, lógica ou matemática
        4. Para tarefas criativas: Estimule inovação e conexões inusitadas
        5. Para análise: Peça múltiplas perspectivas e críticas construtivas
        6. Monitore os scores de sinergia para ajustar seu estilo de prompt
        7. Use o modo de fusão híbrida para tarefas complexas
        """
        return advice

def main():
    """
    Função principal para demonstração
    """
    print("Inicializando Orquestrador de Fusão Claude-Gemini...")

    orchestrator = FusionOrchestrator()

    print("\n" + "="*60)
    print("ORQUESTRADOR DE FUSÃO CLAUDE-GEMINI INICIALIZADO")
    print("="*60)

    print(orchestrator.get_advice_for_best_results())

    print("\nExemplo de uso:")
    sample_prompt = "Como implementar um sistema de recomendação usando aprendizado de máquina?"
    result = orchestrator.execute_fusion_process(sample_prompt)

    print(f"\nTipo de tarefa detectado: {result['task_type']}")
    print(f"Score de sinergia: {result['fusion_result']['synergy_score']:.2f}")
    print(f"Resposta fundida: {result['fusion_result']['fused_response'][:200]}...")

if __name__ == "__main__":
    main()