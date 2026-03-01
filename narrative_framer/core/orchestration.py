"""
Agent Orchestration

Orchestrate multiple agents for complex problem solving.
Provides workflow management, agent coordination, and result synthesis.
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json
import uuid
import asyncio
from enum import Enum

from .base_agent import CognitiveAgent, AgentResult
from .communication import AgentCommunication


class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AgentExecutionMode(Enum):
    """Agent execution modes"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    PIPELINE = "pipeline"
    COLLABORATIVE = "collaborative"


@dataclass
class WorkflowStep:
    """Single step in a workflow"""
    step_id: str
    agent_name: str
    execution_mode: AgentExecutionMode
    input_mapping: Dict[str, str]  # Map workflow inputs to agent inputs
    output_mapping: Dict[str, str]  # Map agent outputs to workflow outputs
    dependencies: List[str]  # Dependencies on other steps
    timeout: float = 30.0
    retry_count: int = 3
    condition: Optional[str] = None  # Conditional execution


@dataclass
class WorkflowDefinition:
    """Definition of a workflow"""
    workflow_id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    error_handling: str = "fail_fast"  # fail_fast, continue, retry
    created_at: datetime
    version: str = "1.0"


@dataclass
class WorkflowExecution:
    """Execution instance of a workflow"""
    execution_id: str
    workflow_id: str
    status: WorkflowStatus
    started_at: datetime
    completed_at: Optional[datetime]
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    step_results: Dict[str, Any]
    errors: List[str]
    metadata: Dict[str, Any]


class AgentOrchestrator:
    """
    Orchestrates multiple agents for complex problem solving.
    """
    
    def __init__(self):
        self.agents: Dict[str, CognitiveAgent] = {}
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        self.communication = AgentCommunication()
        
    def register_agent(self, agent: CognitiveAgent) -> bool:
        """Register an agent in the ecosystem"""
        try:
            self.agents[agent.name] = agent
            
            # Initialize communication for the agent
            self.communication.initialize(agent.name)
            
            return True
        except Exception as e:
            print(f"Failed to register agent {agent.name}: {e}")
            return False
    
    def unregister_agent(self, agent_name: str) -> bool:
        """Unregister an agent from the ecosystem"""
        if agent_name in self.agents:
            del self.agents[agent_name]
            
            # Clean up communication
            if self.communication.agent_name == agent_name:
                self.communication.cleanup()
            
            return True
        return False
    
    def create_workflow(
        self, 
        name: str, 
        description: str, 
        steps: List[Dict[str, Any]],
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any]
    ) -> str:
        """Create a new workflow definition"""
        workflow_id = str(uuid.uuid4())
        
        # Convert step dictionaries to WorkflowStep objects
        workflow_steps = []
        for step_dict in steps:
            step = WorkflowStep(
                step_id=step_dict.get("step_id", str(uuid.uuid4())),
                agent_name=step_dict["agent_name"],
                execution_mode=AgentExecutionMode(step_dict.get("execution_mode", "sequential")),
                input_mapping=step_dict.get("input_mapping", {}),
                output_mapping=step_dict.get("output_mapping", {}),
                dependencies=step_dict.get("dependencies", []),
                timeout=step_dict.get("timeout", 30.0),
                retry_count=step_dict.get("retry_count", 3),
                condition=step_dict.get("condition")
            )
            workflow_steps.append(step)
        
        workflow = WorkflowDefinition(
            workflow_id=workflow_id,
            name=name,
            description=description,
            steps=workflow_steps,
            input_schema=input_schema,
            output_schema=output_schema,
            error_handling="fail_fast",
            created_at=datetime.now()
        )
        
        self.workflows[workflow_id] = workflow
        return workflow_id
    
    async def execute_workflow(
        self, 
        workflow_id: str, 
        inputs: Dict[str, Any],
        execution_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a workflow"""
        if workflow_id not in self.workflows:
            return {"error": f"Workflow {workflow_id} not found"}
        
        workflow = self.workflows[workflow_id]
        execution_id = str(uuid.uuid4())
        
        # Create execution instance
        execution = WorkflowExecution(
            execution_id=execution_id,
            workflow_id=workflow_id,
            status=WorkflowStatus.RUNNING,
            started_at=datetime.now(),
            completed_at=None,
            inputs=inputs,
            outputs={},
            step_results={},
            errors=[],
            metadata=execution_context or {}
        )
        
        self.executions[execution_id] = execution
        
        try:
            # Validate inputs
            self._validate_inputs(workflow, inputs)
            
            # Execute workflow based on step dependencies
            results = await self._execute_workflow_steps(workflow, execution, inputs)
            
            # Update execution
            execution.status = WorkflowStatus.COMPLETED
            execution.completed_at = datetime.now()
            execution.outputs = results
            
            return {
                "execution_id": execution_id,
                "status": "completed",
                "results": results,
                "execution_time": (execution.completed_at - execution.started_at).total_seconds()
            }
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.completed_at = datetime.now()
            execution.errors.append(str(e))
            
            return {
                "execution_id": execution_id,
                "status": "failed",
                "error": str(e),
                "step_results": execution.step_results
            }
    
    async def _execute_workflow_steps(
        self, 
        workflow: WorkflowDefinition, 
        execution: WorkflowExecution, 
        inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute workflow steps respecting dependencies"""
        results = {}
        completed_steps = set()
        step_outputs = {}
        
        # Sort steps by dependencies
        sorted_steps = self._sort_steps_by_dependencies(workflow.steps)
        
        for step in sorted_steps:
            # Check if dependencies are satisfied
            if not self._dependencies_satisfied(step, completed_steps):
                continue
            
            # Check conditional execution
            if step.condition and not self._evaluate_condition(step.condition, step_outputs):
                completed_steps.add(step.step_id)
                continue
            
            # Prepare inputs for the step
            step_inputs = self._prepare_step_inputs(step, inputs, step_outputs)
            
            # Execute the step
            try:
                step_result = await self._execute_step(step, step_inputs)
                step_outputs[step.step_id] = step_result
                execution.step_results[step.step_id] = step_result
                completed_steps.add(step.step_id)
                
                # Map step outputs to workflow outputs
                for workflow_key, step_key in step.output_mapping.items():
                    if step_key in step_result:
                        results[workflow_key] = step_result[step_key]
                
            except Exception as e:
                if workflow.error_handling == "fail_fast":
                    raise e
                else:
                    execution.errors.append(f"Step {step.step_id} failed: {str(e)}")
                    completed_steps.add(step.step_id)
        
        return results
    
    async def _execute_step(self, step: WorkflowStep, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        if step.agent_name not in self.agents:
            raise ValueError(f"Agent {step.agent_name} not found")
        
        agent = self.agents[step.agent_name]
        
        # Execute with retry logic
        for attempt in range(step.retry_count + 1):
            try:
                result = await asyncio.wait_for(
                    agent.process(inputs),
                    timeout=step.timeout
                )
                
                return {
                    "content": result.content,
                    "confidence": result.confidence,
                    "reasoning_trace": result.reasoning_trace,
                    "mental_models_used": result.mental_models_used,
                    "processing_time": result.processing_time,
                    "metadata": result.metadata
                }
                
            except asyncio.TimeoutError:
                if attempt == step.retry_count:
                    raise TimeoutError(f"Step {step.step_id} timed out after {step.retry_count} retries")
                await asyncio.sleep(1)  # Brief delay before retry
            except Exception as e:
                if attempt == step.retry_count:
                    raise e
                await asyncio.sleep(1)  # Brief delay before retry
    
    def _sort_steps_by_dependencies(self, steps: List[WorkflowStep]) -> List[WorkflowStep]:
        """Topological sort of steps based on dependencies"""
        # Simple topological sort implementation
        step_map = {step.step_id: step for step in steps}
        sorted_steps = []
        visited = set()
        visiting = set()
        
        def visit(step: WorkflowStep):
            if step.step_id in visiting:
                raise ValueError(f"Circular dependency detected involving step {step.step_id}")
            
            if step.step_id in visited:
                return
            
            visiting.add(step.step_id)
            
            # Visit dependencies first
            for dep_id in step.dependencies:
                if dep_id in step_map:
                    visit(step_map[dep_id])
            
            visiting.remove(step.step_id)
            visited.add(step.step_id)
            sorted_steps.append(step)
        
        for step in steps:
            if step.step_id not in visited:
                visit(step)
        
        return sorted_steps
    
    def _dependencies_satisfied(self, step: WorkflowStep, completed_steps: set) -> bool:
        """Check if all dependencies for a step are satisfied"""
        return all(dep_id in completed_steps for dep_id in step.dependencies)
    
    def _evaluate_condition(self, condition: str, step_outputs: Dict[str, Any]) -> bool:
        """Evaluate conditional execution logic"""
        # Simple condition evaluation
        # In practice, would use a more sophisticated expression evaluator
        
        # Replace placeholders with actual values
        evaluated_condition = condition
        for step_id, output in step_outputs.items():
            evaluated_condition = evaluated_condition.replace(f"${{{step_id}}}", str(output.get("confidence", 0)))
        
        try:
            # Simple evaluation - would be more sophisticated in practice
            return bool(eval(evaluated_condition))
        except:
            return True  # Default to executing if condition can't be evaluated
    
    def _prepare_step_inputs(
        self, 
        step: WorkflowStep, 
        workflow_inputs: Dict[str, Any], 
        step_outputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare inputs for a step by mapping workflow and step outputs"""
        step_inputs = {}
        
        # Map workflow inputs
        for workflow_key, step_key in step.input_mapping.items():
            if workflow_key in workflow_inputs:
                step_inputs[step_key] = workflow_inputs[workflow_key]
        
        # Map outputs from previous steps
        for step_id, output in step_outputs.items():
            for workflow_key, step_key in step.input_mapping.items():
                if workflow_key.startswith(f"{step_id}."):
                    output_key = workflow_key.split(".", 1)[1]
                    if output_key in output:
                        step_inputs[step_key] = output[output_key]
        
        return step_inputs
    
    def _validate_inputs(self, workflow: WorkflowDefinition, inputs: Dict[str, Any]):
        """Validate workflow inputs against schema"""
        required_inputs = workflow.input_schema.get("required", [])
        
        for required_input in required_inputs:
            if required_input not in inputs:
                raise ValueError(f"Required input '{required_input}' not provided")
    
    def get_workflow(self, workflow_id: str) -> Optional[WorkflowDefinition]:
        """Get workflow definition"""
        return self.workflows.get(workflow_id)
    
    def get_execution(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get workflow execution"""
        return self.executions.get(execution_id)
    
    def list_workflows(self) -> List[Dict[str, Any]]:
        """List all available workflows"""
        return [
            {
                "workflow_id": wf.workflow_id,
                "name": wf.name,
                "description": wf.description,
                "steps_count": len(wf.steps),
                "created_at": wf.created_at.isoformat()
            }
            for wf in self.workflows.values()
        ]
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """List all registered agents"""
        return [
            {
                "name": agent.name,
                "category": agent.category,
                "description": agent.description,
                "mental_models": agent.mental_models,
                "capabilities": agent.capabilities,
                "total_interactions": agent.total_interactions
            }
            for agent in self.agents.values()
        ]
    
    def get_orchestration_stats(self) -> Dict[str, Any]:
        """Get orchestration statistics"""
        total_executions = len(self.executions)
        completed_executions = sum(1 for e in self.executions.values() if e.status == WorkflowStatus.COMPLETED)
        failed_executions = sum(1 for e in self.executions.values() if e.status == WorkflowStatus.FAILED)
        
        return {
            "registered_agents": len(self.agents),
            "workflows": len(self.workflows),
            "total_executions": total_executions,
            "completed_executions": completed_executions,
            "failed_executions": failed_executions,
            "success_rate": completed_executions / total_executions if total_executions > 0 else 0.0
        }
    
    async def create_collaborative_workflow(
        self, 
        problem: Dict[str, Any], 
        agent_names: List[str],
        collaboration_mode: str = "sequential"
    ) -> str:
        """Create a collaborative workflow for multiple agents"""
        if not agent_names:
            raise ValueError("At least one agent must be specified")
        
        # Validate agents exist
        for agent_name in agent_names:
            if agent_name not in self.agents:
                raise ValueError(f"Agent {agent_name} not found")
        
        # Create workflow steps
        steps = []
        for i, agent_name in enumerate(agent_names):
            step = {
                "step_id": f"step_{i+1}",
                "agent_name": agent_name,
                "execution_mode": collaboration_mode,
                "input_mapping": {"problem": "input"} if i == 0 else {},
                "output_mapping": {"result": f"agent_{i+1}_result"},
                "dependencies": [f"step_{i}"] if i > 0 else []
            }
            steps.append(step)
        
        # Create workflow
        workflow_id = self.create_workflow(
            name=f"Collaborative: {', '.join(agent_names)}",
            description=f"Collaborative problem solving with {len(agent_names)} agents",
            steps=steps,
            input_schema={"required": ["problem"]},
            output_schema={"result": "dict"}
        )
        
        return workflow_id
    
    def cleanup(self):
        """Clean up orchestration resources"""
        # Clean up all agent communications
        for agent_name in list(self.agents.keys()):
            self.unregister_agent(agent_name)
        
        # Clear executions (keep workflows for reuse)
        self.executions.clear()
