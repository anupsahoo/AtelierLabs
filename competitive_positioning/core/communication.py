"""
Agent Communication Protocol

Enables inter-agent communication and collaboration.
Provides structured messaging, message passing, and coordination capabilities.
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import json
import uuid
import asyncio
from enum import Enum


class MessageType(Enum):
    """Types of messages between agents"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    COLLABORATION = "collaboration"
    FEEDBACK = "feedback"
    STATUS_UPDATE = "status_update"


class MessagePriority(Enum):
    """Message priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Message:
    """Structured message for agent communication"""
    id: str
    sender: str
    recipient: str
    message_type: MessageType
    priority: MessagePriority
    content: Dict[str, Any]
    timestamp: datetime
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": self.message_type.value,
            "priority": self.priority.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id,
            "reply_to": self.reply_to,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary"""
        return cls(
            id=data["id"],
            sender=data["sender"],
            recipient=data["recipient"],
            message_type=MessageType(data["message_type"]),
            priority=MessagePriority(data["priority"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            correlation_id=data.get("correlation_id"),
            reply_to=data.get("reply_to"),
            expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
            metadata=data.get("metadata", {})
        )


class MessageBus:
    """Central message bus for agent communication"""
    
    def __init__(self):
        self.messages: Dict[str, Message] = {}
        self.queues: Dict[str, List[Message]] = {}
        self.subscribers: Dict[str, List[str]] = {}
        self.message_handlers: Dict[str, Callable] = {}
        
    def send_message(self, message: Message) -> bool:
        """Send a message through the bus"""
        try:
            # Store message
            self.messages[message.id] = message
            
            # Add to recipient's queue
            if message.recipient not in self.queues:
                self.queues[message.recipient] = []
            self.queues[message.recipient].append(message)
            
            # Notify subscribers
            self._notify_subscribers(message)
            
            # Call message handler if registered
            if message.recipient in self.message_handlers:
                asyncio.create_task(self.message_handlers[message.recipient](message))
            
            return True
        except Exception as e:
            print(f"Failed to send message: {e}")
            return False
    
    def receive_messages(self, agent_name: str, limit: int = 10) -> List[Message]:
        """Receive messages for an agent"""
        if agent_name not in self.queues:
            return []
        
        messages = self.queues[agent_name][:limit]
        self.queues[agent_name] = self.queues[agent_name][limit:]
        
        # Filter expired messages
        current_time = datetime.now()
        valid_messages = [
            msg for msg in messages 
            if msg.expires_at is None or msg.expires_at > current_time
        ]
        
        return valid_messages
    
    def subscribe(self, agent_name: str, message_type: str) -> bool:
        """Subscribe to specific message types"""
        if message_type not in self.subscribers:
            self.subscribers[message_type] = []
        
        if agent_name not in self.subscribers[message_type]:
            self.subscribers[message_type].append(agent_name)
            return True
        
        return False
    
    def unsubscribe(self, agent_name: str, message_type: str) -> bool:
        """Unsubscribe from message types"""
        if message_type in self.subscribers:
            if agent_name in self.subscribers[message_type]:
                self.subscribers[message_type].remove(agent_name)
                return True
        
        return False
    
    def register_handler(self, agent_name: str, handler: Callable) -> bool:
        """Register message handler for an agent"""
        try:
            self.message_handlers[agent_name] = handler
            return True
        except Exception as e:
            print(f"Failed to register handler: {e}")
            return False
    
    def _notify_subscribers(self, message: Message):
        """Notify subscribers of message type"""
        message_type = message.message_type.value
        if message_type in self.subscribers:
            for subscriber in self.subscribers[message_type]:
                if subscriber != message.recipient:  # Don't notify sender
                    # Add copy to subscriber's queue
                    if subscriber not in self.queues:
                        self.queues[subscriber] = []
                    
                    notification = Message(
                        id=str(uuid.uuid4()),
                        sender="message_bus",
                        recipient=subscriber,
                        message_type=MessageType.NOTIFICATION,
                        priority=MessagePriority.LOW,
                        content={
                            "original_message_id": message.id,
                            "message_type": message_type,
                            "sender": message.sender,
                            "recipient": message.recipient
                        },
                        timestamp=datetime.now()
                    )
                    
                    self.queues[subscriber].append(notification)
    
    def get_message_stats(self) -> Dict[str, Any]:
        """Get message bus statistics"""
        return {
            "total_messages": len(self.messages),
            "queues": {agent: len(messages) for agent, messages in self.queues.items()},
            "subscribers": {msg_type: len(subs) for msg_type, subs in self.subscribers.items()},
            "registered_handlers": len(self.message_handlers)
        }


class CommunicationProtocol:
    """Protocol for structured agent communication"""
    
    def __init__(self, message_bus: MessageBus):
        self.message_bus = message_bus
        self.pending_requests: Dict[str, asyncio.Future] = {}
        
    async def send_request(
        self, 
        sender: str, 
        recipient: str, 
        request_content: Dict[str, Any],
        priority: MessagePriority = MessagePriority.MEDIUM,
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """Send a request and wait for response"""
        correlation_id = str(uuid.uuid4())
        
        # Create request message
        request = Message(
            id=str(uuid.uuid4()),
            sender=sender,
            recipient=recipient,
            message_type=MessageType.REQUEST,
            priority=priority,
            content=request_content,
            timestamp=datetime.now(),
            correlation_id=correlation_id
        )
        
        # Create future for response
        future = asyncio.Future()
        self.pending_requests[correlation_id] = future
        
        # Send request
        success = self.message_bus.send_message(request)
        
        if not success:
            future.set_exception(Exception("Failed to send request"))
            del self.pending_requests[correlation_id]
            return {"error": "Failed to send request"}
        
        try:
            # Wait for response
            response = await asyncio.wait_for(future, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            del self.pending_requests[correlation_id]
            return {"error": "Request timed out"}
        except Exception as e:
            del self.pending_requests[correlation_id]
            return {"error": str(e)}
    
    async def send_response(
        self, 
        sender: str, 
        original_message: Message, 
        response_content: Dict[str, Any]
    ) -> bool:
        """Send a response to a request"""
        response = Message(
            id=str(uuid.uuid4()),
            sender=sender,
            recipient=original_message.sender,
            message_type=MessageType.RESPONSE,
            priority=original_message.priority,
            content=response_content,
            timestamp=datetime.now(),
            correlation_id=original_message.correlation_id,
            reply_to=original_message.id
        )
        
        return self.message_bus.send_message(response)
    
    async def send_notification(
        self, 
        sender: str, 
        recipient: str, 
        notification_content: Dict[str, Any],
        priority: MessagePriority = MessagePriority.LOW
    ) -> bool:
        """Send a notification (no response expected)"""
        notification = Message(
            id=str(uuid.uuid4()),
            sender=sender,
            recipient=recipient,
            message_type=MessageType.NOTIFICATION,
            priority=priority,
            content=notification_content,
            timestamp=datetime.now()
        )
        
        return self.message_bus.send_message(notification)
    
    async def broadcast_message(
        self, 
        sender: str, 
        broadcast_content: Dict[str, Any],
        priority: MessagePriority = MessagePriority.MEDIUM
    ) -> int:
        """Broadcast message to all subscribed agents"""
        # Get all agents with queues
        all_agents = set(self.message_bus.queues.keys())
        all_agents.discard(sender)  # Don't send to self
        
        success_count = 0
        for agent in all_agents:
            message = Message(
                id=str(uuid.uuid4()),
                sender=sender,
                recipient=agent,
                message_type=MessageType.NOTIFICATION,
                priority=priority,
                content={**broadcast_content, "broadcast": True},
                timestamp=datetime.now()
            )
            
            if self.message_bus.send_message(message):
                success_count += 1
        
        return success_count
    
    def handle_response(self, message: Message):
        """Handle incoming response messages"""
        if message.correlation_id and message.correlation_id in self.pending_requests:
            future = self.pending_requests[message.correlation_id]
            
            if not future.done():
                future.set_result(message.content)
            
            del self.pending_requests[message.correlation_id]
    
    def register_agent(self, agent_name: str) -> bool:
        """Register an agent for communication"""
        # Subscribe to all message types
        for message_type in MessageType:
            self.message_bus.subscribe(agent_name, message_type.value)
        
        # Register message handler
        async def message_handler(message: Message):
            await self._handle_incoming_message(agent_name, message)
        
        return self.message_bus.register_handler(agent_name, message_handler)
    
    async def _handle_incoming_message(self, agent_name: str, message: Message):
        """Handle incoming messages for an agent"""
        if message.message_type == MessageType.RESPONSE:
            self.handle_response(message)
        # Other message types would be handled by the agent itself
        # This is a placeholder for agent-specific message handling


class AgentCommunication:
    """
    High-level communication interface for agents.
    """
    
    def __init__(self):
        self.message_bus = MessageBus()
        self.protocol = CommunicationProtocol(self.message_bus)
        self.agent_name = None
        self.registered = False
    
    def initialize(self, agent_name: str) -> bool:
        """Initialize communication for an agent"""
        self.agent_name = agent_name
        self.registered = self.protocol.register_agent(agent_name)
        return self.registered
    
    async def send_message(
        self, 
        recipient: str, 
        message_type: str, 
        content: Dict[str, Any],
        priority: str = "medium",
        expect_response: bool = False,
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """Send a message to another agent"""
        if not self.registered:
            return {"error": "Agent not registered for communication"}
        
        try:
            priority_enum = MessagePriority(priority.lower())
        except ValueError:
            priority_enum = MessagePriority.MEDIUM
        
        if expect_response:
            return await self.protocol.send_request(
                self.agent_name, recipient, content, priority_enum, timeout
            )
        else:
            success = await self.protocol.send_notification(
                self.agent_name, recipient, content, priority_enum
            )
            return {"success": success}
    
    async def broadcast_message(
        self, 
        content: Dict[str, Any], 
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """Broadcast message to all agents"""
        if not self.registered:
            return {"error": "Agent not registered for communication"}
        
        try:
            priority_enum = MessagePriority(priority.lower())
        except ValueError:
            priority_enum = MessagePriority.MEDIUM
        
        success_count = await self.protocol.broadcast_message(
            self.agent_name, content, priority_enum
        )
        
        return {
            "success": True,
            "recipients": success_count
        }
    
    def receive_messages(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Receive pending messages"""
        if not self.registered:
            return []
        
        messages = self.message_bus.receive_messages(self.agent_name, limit)
        return [msg.to_dict() for msg in messages]
    
    async def collaborate(self, agents: List[str], problem: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate collaboration with multiple agents"""
        if not self.registered:
            return {"error": "Agent not registered for communication"}
        
        collaboration_id = str(uuid.uuid4())
        results = {}
        
        # Send collaboration requests to all agents
        tasks = []
        for agent in agents:
            if agent != self.agent_name:
                task = self.send_message(
                    agent, 
                    "collaboration", 
                    {
                        "collaboration_id": collaboration_id,
                        "problem": problem,
                        "role": "collaborator"
                    },
                    priority="high",
                    expect_response=True
                )
                tasks.append(task)
        
        # Wait for all responses
        if tasks:
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, agent in enumerate(agents):
                if agent != self.agent_name:
                    results[agent] = responses[i]
        
        return {
            "collaboration_id": collaboration_id,
            "participants": agents,
            "results": results
        }
    
    def get_communication_stats(self) -> Dict[str, Any]:
        """Get communication statistics"""
        return self.message_bus.get_message_stats()
    
    def cleanup(self):
        """Clean up communication resources"""
        if self.agent_name:
            # Unsubscribe from all message types
            for message_type in MessageType:
                self.message_bus.unsubscribe(self.agent_name, message_type.value)
            
            # Remove message handler
            if self.agent_name in self.message_bus.message_handlers:
                del self.message_bus.message_handlers[self.agent_name]
            
            # Clear message queue
            if self.agent_name in self.message_bus.queues:
                del self.message_bus.queues[self.agent_name]
            
            self.registered = False
