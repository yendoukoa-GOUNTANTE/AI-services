import React, { useState, useEffect } from 'react';
import {
  Search,
  User as UserIcon,
  Zap,
  Wrench,
  ShieldCheck,
  Cpu,
  Globe,
  CreditCard,
  Menu,
  X,
  AlertCircle,
  Key,
  Gamepad2,
  Database,
  Code2,
  Scale,
  Stethoscope,
  Plane,
  Music,
  ShoppingBag,
  ShieldAlert,
  ShieldX,
  Binary,
  Bot,
  FlaskConical,
  Truck,
  Building2,
  BookOpen,
  Microscope,
  Layout,
  Mail,
  TrendingUp,
  Smartphone,
  Cloud,
  Server,
  DollarSign,
  Handshake,
  PiggyBank,
  Brain,
  Camera,
  Video,
  Settings,
  Route,
  Mic,
  FileText,
  Download,
  Trash2,
  Save,
  Plus
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { userService, aiService, paymentService, fileService, storeService, setAuthToken, type User, type File, type StoreAgent, type StoreDesign } from './api';
import axios from 'axios';

interface AIService {
  id: string | number;
  name: string;
  category: string;
  icon: LucideIcon;
  description: string;
  featured?: boolean;
  isStoreItem?: boolean;
  type?: 'agent' | 'design';
  price?: number;
}

const AI_SERVICES: AIService[] = [
  { id: 'website', name: 'Software Engineering', category: 'Development', icon: Globe, description: 'Professional software engineering and multi-section website generation.', featured: true },
  { id: 'conflict-debug', name: 'Debugger', category: 'Development', icon: ShieldCheck, description: 'Elite code debugging and multi-model conflict resolution specialist.', featured: true },
  { id: 'marketing', name: 'Marketer', category: 'Business', icon: Mail, description: 'Expert marketing bot management and high-fidelity video generation.', featured: true },
  { id: 'system-analyzer', name: 'System Analyser', category: 'Infrastructure', icon: Search, description: 'Advanced system analysis, broken link detection, and infrastructure audits.', featured: true },
  { id: 'antigravity', name: 'Antigravity Agent', category: 'Advanced', icon: Bot, description: 'Elite agentic development with secure Linux sandbox execution and reasoning.' },
  { id: 'gemini-spark', name: 'Gemini Spark', category: 'Advanced', icon: Zap, description: '24/7 personal AI agent for autonomous multi-step tasks and workspace intelligence.' },
  { id: 'copilot-coding', name: 'GitHub Copilot Expert', category: 'Development', icon: Code2, description: 'Elite code generation, refactoring, and debugging powered by GitHub Models.' },
  { id: 'deepmind-image', name: 'DeepMind Image Gen', category: 'Arts', icon: Camera, description: 'Generate stunning high-fidelity images using DeepMind Imagen technology.' },
  { id: 'deepmind-video', name: 'DeepMind Video Creator', category: 'Arts', icon: Video, description: 'Advanced cinematic content, scripts, and storyboards powered by DeepMind.' },
  { id: 'cyber-sentinel', name: 'Cybersecurity Sentinel', category: 'Security', icon: ShieldCheck, description: 'Elite security audits, penetration testing guidance, and real-time threat intelligence.' },
  { id: 'togo-gov', name: 'Togo Public Service', category: 'Public', icon: Building2, description: 'Elite AI for Togolese public services, government administration, and national security.' },
  { id: 'llama-intel', name: 'Llama 3.1 Intelligence', category: 'Advanced', icon: Brain, description: 'Deep reasoning and data-driven insights powered by Meta Llama 3.1 405B.' },
  { id: 'langflow', name: 'Langflow Executor', category: 'Advanced', icon: Zap, description: 'Execute complex AI workflows using Langflow.' },
  { id: 'game', name: 'Game Developer', category: 'Development', icon: Gamepad2, description: 'Create custom games using AI technologies.' },
  { id: 'backend', name: 'Backend Architect', category: 'Infrastructure', icon: Database, description: 'Generate robust Python/Flask backends.' },
  { id: 'blockchain', name: 'Blockchain Expert', category: 'Development', icon: Code2, description: 'Smart contract and blockchain solutions.' },
  { id: 'fintech', name: 'Fintech Strategist', category: 'Business', icon: CreditCard, description: 'Banking and financial technology consulting.' },
  { id: 'legal', name: 'Legal & Human Rights', category: 'Professional', icon: Scale, description: 'Expert legal research and advocacy support.' },
  { id: 'diagnostic', name: 'Medical Diagnostic', category: 'Health', icon: Stethoscope, description: 'Expert diagnostic assistance for all diseases, focusing on cancer and heart disease.' },
  { id: 'aerospace', name: 'Aerospace & Auto', category: 'Engineering', icon: Plane, description: 'Aeronautics and automotive technical guidance.' },
  { id: 'music', name: 'Music Producer', category: 'Arts', icon: Music, description: 'Beat production and artist marketing.' },
  { id: 'eshop', name: 'E-commerce Guru', category: 'Business', icon: ShoppingBag, description: 'Create and manage high-performing e-shops.' },
  { id: 'investigation', name: 'Cyber Investigator', category: 'Security', icon: ShieldAlert, description: 'Digital forensics and security investigation.' },
  { id: 'ml-expert', name: 'Machine Learning', category: 'Development', icon: Binary, description: 'Algorithm selection and model optimization.' },
  { id: 'biotech', name: 'Biotech Specialist', category: 'Science', icon: FlaskConical, description: 'Molecular biology and regulatory research.' },
  { id: 'logistics', name: 'Logistics Manager', category: 'Business', icon: Truck, description: 'Route optimization and movement management.' },
  { id: 'it-ops', name: 'IT Operations', category: 'Infrastructure', icon: Cpu, description: 'Server and network administration.' },
  { id: 'gov-admin', name: 'Gov Administrator', category: 'Public', icon: Building2, description: 'Navigating government services and documents.' },
  { id: 'gov-policy', name: 'Policy Advisor', category: 'Public', icon: Scale, description: 'Public policy analysis and strategic recommendations.' },
  { id: 'gov-engagement', name: 'Citizen Engagement', category: 'Public', icon: UserIcon, description: 'Strategies for civic participation and consultations.' },
  { id: 'gov-smart-city', name: 'Smart City Strategist', category: 'Public', icon: Zap, description: 'Urban tech integration and data-driven infrastructure.' },
  { id: 'gov-bias-detection', name: 'Bias Detector', category: 'Public', icon: ShieldAlert, description: 'Analyze government services and policies for AI bias and ethical fairness.' },
  { id: 'military', name: 'Military Strategist', category: 'Public', icon: ShieldCheck, description: 'Defense analysis and strategic operational planning.' },
  { id: 'gendarmerie', name: 'Gendarmerie Advisor', category: 'Public', icon: ShieldCheck, description: 'Specialized paramilitary and rural security guidance.' },
  { id: 'police', name: 'Police Specialist', category: 'Public', icon: ShieldCheck, description: 'Optimizing law enforcement and community policing.' },
  { id: 'security-opt', name: 'Security Optimizer', category: 'Public', icon: Zap, description: 'Performance tuning for public security services.' },
  { id: 'education', name: 'Science Educator', category: 'Academic', icon: BookOpen, description: 'Mathematics, physics, and biology education.' },
  { id: 'verification', name: 'Content Verifier', category: 'Security', icon: ShieldCheck, description: 'AI content and fake news detection.' },
  { id: 'maintenance', name: 'Hardware Expert', category: 'Support', icon: Wrench, description: 'Software & hardware troubleshooting.' },
  { id: 'digital-repair', name: 'Digital Repair', category: 'Support', icon: Wrench, description: 'Troubleshooting media, apps, and websites.' },
  { id: 'researcher', name: 'AI Researcher', category: 'Science', icon: Microscope, description: 'State-of-the-art AI methodology research.' },
  { id: 'google-sites', name: 'Google Sites Specialist', category: 'Infrastructure', icon: Layout, description: 'Google Sites & DNS configuration expert.' },
  { id: 'investment', name: 'Investment Specialist', category: 'Business', icon: TrendingUp, description: 'Investment optimization and trading assistance.' },
  { id: 'autogpt', name: 'AutoGPT Agent', category: 'Advanced', icon: Bot, description: 'Autonomous agent for multi-step task planning and strategy.' },
  { id: 'cloud-infra', name: 'Cloud Infra Architect', category: 'Infrastructure', icon: Server, description: 'Expert in secure IPs, DNS, and cloud server creation.' },
  { id: 'domain-codex', name: 'Domain Codex Designer', category: 'Infrastructure', icon: Layout, description: 'Elite custom domain design and USSP infrastructure architect.' },
  { id: 'iaas', name: 'IaaS Specialist', category: 'Infrastructure', icon: Cpu, description: 'Infrastructure as a Service expert for virtualized resources.' },
  { id: 'paas', name: 'PaaS Specialist', category: 'Infrastructure', icon: Cloud, description: 'Platform as a Service expert for application development environments.' },
  { id: 'saas', name: 'SaaS Specialist', category: 'Infrastructure', icon: Globe, description: 'Software as a Service expert for internet-delivered applications.' },
  { id: 'itaas', name: 'ITaaS Specialist', category: 'Infrastructure', icon: Layout, description: 'IT as a Service expert for comprehensive IT service delivery.' },
  { id: 'gumloop', name: 'Gumloop Expert', category: 'Advanced', icon: Zap, description: 'Elite AI-powered browser automation and workflow specialist.' },
  { id: 'n8n', name: 'n8n Architect', category: 'Advanced', icon: Cpu, description: 'Elite fair-code workflow automation and node configuration specialist.' },
  { id: 'lamatic', name: 'Lamatic.ai Specialist', category: 'Advanced', icon: Bot, description: 'Elite Generative AI app platform and RAG pipeline specialist.' },
  { id: 'automl-feat', name: 'AutoML Feature Eng', category: 'Development', icon: Binary, description: 'Automated feature engineering and data preparation.' },
  { id: 'automl-tune', name: 'AutoML Tuner', category: 'Development', icon: TrendingUp, description: 'Automated hyperparameter optimization and tuning.' },
  { id: 'automl-select', name: 'AutoML Selector', category: 'Development', icon: Microscope, description: 'Automated model selection and evaluation.' },
  { id: 'automl-mlops', name: 'AutoML MLOps', category: 'Development', icon: Zap, description: 'Automated ML pipelines and MLOps strategy.' },
  { id: 'monetization', name: 'Monetization Expert', category: 'Business', icon: DollarSign, description: 'Strategic advice on revenue generation and subscriptions.' },
  { id: 'partnership', name: 'Partnership Specialist', category: 'Business', icon: Handshake, description: 'Identify and nurture strategic business alliances.' },
  { id: 'fundraising', name: 'Fundraising Strategist', category: 'Business', icon: PiggyBank, description: 'Comprehensive plans for securing project funding.' },
  { id: 'llama-guard', name: 'Llama Guard', category: 'Security', icon: ShieldCheck, description: 'AI safety and content moderation using Meta Llama Guard 3.' },
  { id: 'nemotron', name: 'Nemotron-4 Reasoner', category: 'Advanced', icon: Zap, description: 'Elite reasoning and complex problem solving powered by NVIDIA Nemotron-4 340B.' },
  { id: 'mixtral', name: 'Mixtral Multilingual', category: 'Advanced', icon: Globe, description: 'High-quality multilingual assistance powered by Mixtral 8x7B.' },
  { id: 'claude-intel', name: 'Claude 3.5 Intelligence', category: 'Advanced', icon: Brain, description: 'Deep reasoning and strategic analysis powered by Anthropic Claude 3.5 Sonnet.' },
  { id: 'claude-coder', name: 'Claude 3.5 Coder', category: 'Development', icon: Code2, description: 'Elite code generation and architectural advice powered by Anthropic Claude 3.5 Sonnet.' },
  { id: 'malware-defense', name: 'Malware Defender', category: 'Security', icon: ShieldX, description: 'Elite specialist for detecting, preventing, and removing all types of malware.' },
  { id: 'ussd-blockchain', name: 'USSD Blockchain Expert', category: 'Development', icon: Smartphone, description: 'Design and create USSD applications integrated with blockchain technology.' },
  { id: 'fine-tuner', name: 'Fine-Tuning Specialist', category: 'Development', icon: Settings, description: 'Expert guidance on dataset preparation and fine-tuning Large Language Models.' },
  { id: 'rag-tuning', name: 'RAG & Fine-Tuning Hub', category: 'Advanced', icon: Database, description: 'Elite hybrid AI architectures combining retrieval-augmented generation and specialized fine-tuning.' },
  { id: 'router-capacity', name: 'Router Capacity Architect', category: 'Advanced', icon: Route, description: 'Intelligent LLM routing and automated capacity management.' },
  { id: 'visual-intel', name: 'Visual Intelligence', category: 'Advanced', icon: Camera, description: 'Analyze images and videos captured from your camera to provide insights and descriptions.' },
  { id: 'video-producer', name: 'Video Producer', category: 'Arts', icon: Video, description: 'Expert guidance on scriptwriting, filming, and post-production for professional videos.' },
  { id: 'github-models', name: 'GitHub Models', category: 'Advanced', icon: Cpu, description: 'Access top AI models (GPT-4o, Llama 3, Phi) via the GitHub Models marketplace.' },
  { id: 'copilot-chat', name: 'Copilot Chat API', category: 'Development', icon: Code2, description: 'Direct programmatic access to GitHub Copilot Chat intelligence.' },
  { id: 'podcast', name: 'Podcast Specialist', category: 'Arts', icon: Mic, description: 'Elite podcast production, design, and business strategy guidance.' },
  { id: 'zapier', name: 'Zapier Automation', category: 'Advanced', icon: Zap, description: 'Expert Zapier automation specialized for French-speaking markets.' },
  { id: 'odoo', name: 'Odoo ERP Specialist', category: 'Professional', icon: Layout, description: 'Elite Odoo implementation and customization for Francophone regions.' },
  { id: 'sage', name: 'Sage Software Expert', category: 'Professional', icon: Database, description: 'Expert guidance on Sage accounting and payroll for French businesses.' },
  { id: 'open-collective', name: 'Open Collective Specialist', category: 'Business', icon: DollarSign, description: 'Elite guidance on transparent project funding and community-led financial management.' },
  { id: 'patreon', name: 'Patreon Strategist', category: 'Business', icon: DollarSign, description: 'Expert creator monetization, membership tiers, and audience engagement strategies.' }
];

const App: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('marketplace');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [user, setUser] = useState<User | null>(null);
  const [credits, setCredits] = useState(0);
  const [storeAgents, setStoreAgents] = useState<StoreAgent[]>([]);
  const [storeDesigns, setStoreDesigns] = useState<StoreDesign[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [modalMode, setModalMode] = useState<'login' | 'register'>('register');
  const [username, setUsername] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [userFiles, setUserFiles] = useState<File[]>([]);
  const [selectedService, setSelectedService] = useState<AIService | null>(null);
  const [showServiceModal, setShowServiceModal] = useState(false);
  const [servicePrompt, setServicePrompt] = useState('');
  const [serviceResponse, setServiceResponse] = useState('');
  const [executionParams, setExecutionParams] = useState<any>({});
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [capturedMedia, setCapturedMedia] = useState<{data: string, type: string} | null>(null);
  const [showAgentRegModal, setShowAgentRegModal] = useState(false);
  const [showDesignRegModal, setShowDesignRegModal] = useState(false);
  const [newAgent, setNewAgent] = useState({ name: '', description: '', endpoint_url: '', price_per_use: 50, category: 'General' });
  const [newDesign, setNewDesign] = useState({ name: '', description: '', price: 500, category: 'Web', content: '', preview_url: '' });
  const videoRef = React.useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = React.useRef<MediaRecorder | null>(null);
  const chunksRef = React.useRef<Blob[]>([]);

  useEffect(() => {
    const savedApiKey = localStorage.getItem('globalApiKey');
    if (savedApiKey) {
      setAuthToken(savedApiKey);
      fetchUserData();
    }
    fetchStoreData();
  }, []);

  const fetchStoreData = async () => {
    try {
      const [agentsRes, designsRes] = await Promise.all([
        storeService.getAgents(),
        storeService.getDesigns()
      ]);
      setStoreAgents(agentsRes.data);
      setStoreDesigns(designsRes.data);
    } catch (err) {
      console.error('Failed to fetch store data', err);
    }
  };

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const response = await userService.getMe();
      setUser(response.data);
      setCredits(response.data.credits || 1000);
      setError(null);
      fetchUserFiles();
    } catch (err) {
      console.error('Failed to fetch user data', err);
      setError('Invalid API Key or Session Expired');
      localStorage.removeItem('globalApiKey');
      setAuthToken(null);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const fetchUserFiles = async () => {
    try {
      const res = await fileService.getFiles();
      setUserFiles(res.data);
    } catch (err) {
      console.error('Failed to fetch files', err);
    }
  };

  const handleSaveToStorage = async () => {
    if (!serviceResponse || !selectedService) return;
    try {
      setLoading(true);
      const filename = `${selectedService.name.replace(/\s+/g, '_')}_${Date.now()}.txt`;
      await fileService.createDoc(filename, serviceResponse);
      alert('Saved to storage successfully!');
      fetchUserFiles();
    } catch (err) {
      setError('Failed to save to storage');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      setLoading(true);
      await fileService.uploadFile(file);
      fetchUserFiles();
    } catch (err) {
      setError('Failed to upload file');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteFile = async (id: number) => {
    if (!confirm('Are you sure you want to delete this file?')) return;
    try {
      setLoading(true);
      await fileService.deleteFile(id);
      fetchUserFiles();
    } catch (err) {
      setError('Failed to delete file');
    } finally {
      setLoading(false);
    }
  };

  const handleAgentRegistration = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      await storeService.registerAgent(newAgent);
      alert('Agent registered successfully!');
      setShowAgentRegModal(false);
      fetchStoreData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to register agent');
    } finally {
      setLoading(false);
    }
  };

  const handleDesignRegistration = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      await storeService.registerDesign(newDesign);
      alert('Design registered successfully!');
      setShowDesignRegModal(false);
      fetchStoreData();
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to register design');
    } finally {
      setLoading(false);
    }
  };

  const handleServiceExecution = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) {
      setShowLoginModal(true);
      return;
    }
    if (!servicePrompt || !selectedService) return;

    try {
      setLoading(true);
      setError(null);
      let response;
      const mediaData = capturedMedia?.data.split(',')[1];
      const mimeType = capturedMedia?.type;

      if (selectedService.isStoreItem) {
         if (selectedService.type === 'agent') {
            response = await storeService.executeAgent(selectedService.id as number, servicePrompt);
         } else {
            response = await storeService.purchaseDesign(selectedService.id as number);
         }
      } else {
      switch (selectedService.id) {
        case 'visual-intel':
          response = await aiService.getVisualAnalysis(servicePrompt, mediaData, mimeType);
          break;
        case 'website':
          response = await aiService.generateWebsite(servicePrompt);
          break;
        case 'system-analyzer':
          response = await aiService.analyzeWebsite(servicePrompt);
          break;
        case 'google-sites':
          response = await aiService.getGoogleSitesAssistance(servicePrompt);
          break;
        case 'fintech':
          response = await aiService.getFinancialAdvice(servicePrompt);
          break;
        case 'diagnostic':
          response = await aiService.getDiagnosticAssistance(servicePrompt);
          break;
        case 'marketing':
          if (executionParams.type === 'video') {
            response = await aiService.generateMarketingVideo(servicePrompt);
          } else {
            response = await aiService.getMarketingAssistance(servicePrompt);
          }
          break;
        case 'digital-repair':
          response = await aiService.getDigitalRepairAssistance(servicePrompt);
          break;
        case 'investment':
          response = await aiService.getInvestmentTradingAssistance(servicePrompt);
          break;
        case 'autogpt':
          response = await aiService.getAutoGPTAssistance(servicePrompt);
          break;
        case 'cloud-infra':
          response = await aiService.getCloudInfrastructureAssistance(servicePrompt);
          break;
        case 'domain-codex':
          response = await aiService.getDomainCodexAssistance(servicePrompt);
          break;
        case 'iaas':
          response = await aiService.getIaaSAssistance(servicePrompt);
          break;
        case 'paas':
          response = await aiService.getPaaSAssistance(servicePrompt);
          break;
        case 'saas':
          response = await aiService.getSaaSAssistance(servicePrompt);
          break;
        case 'itaas':
          response = await aiService.getITaaSAssistance(servicePrompt);
          break;
        case 'gumloop':
          response = await aiService.getGumloopAssistance(servicePrompt, executionParams.execute, executionParams.pipeline_id, executionParams.inputs);
          break;
        case 'n8n':
          response = await aiService.getN8nAssistance(servicePrompt, executionParams.execute, executionParams.webhook_url, executionParams.payload);
          break;
        case 'lamatic':
          response = await aiService.getLamaticAssistance(servicePrompt, executionParams.execute, executionParams.workflow_id);
          break;
        case 'malware-defense':
          response = await aiService.getMalwareDefenseAssistance(servicePrompt);
          break;
        case 'ussd-blockchain':
          response = await aiService.getUSSDBlockchainAssistance(servicePrompt);
          break;
        case 'fine-tuner':
          response = await aiService.getFineTuningAssistance(servicePrompt);
          break;
        case 'rag-tuning':
          response = await aiService.getRAGTuningAssistance(servicePrompt);
          break;
        case 'router-capacity':
          response = await aiService.getRouterCapacityAssistance(servicePrompt);
          break;
        case 'antigravity':
          response = await aiService.getAntigravityAgentAssistance(servicePrompt);
          break;
        case 'gemini-spark':
          response = await aiService.getGeminiSparkAssistance(servicePrompt);
          break;
        case 'open-collective':
          response = await aiService.getOpenCollectiveAssistance(servicePrompt);
          break;
        case 'patreon':
          response = await aiService.getPatreonAssistance(servicePrompt);
          break;
        case 'video-producer':
          response = await aiService.getVideoProductionAssistance(servicePrompt);
          break;
        case 'deepmind-image':
          response = await aiService.getDeepMindImage(servicePrompt);
          if (response.data.image_data) {
             setCapturedMedia({ data: `data:image/jpeg;base64,${response.data.image_data}`, type: 'image/jpeg' });
          }
          break;
        case 'deepmind-video':
          response = await aiService.getDeepMindVideo(servicePrompt);
          break;
        case 'podcast':
          response = await aiService.getPodcastAssistance(servicePrompt);
          break;
        case 'zapier':
          response = await aiService.getZapierAssistance(servicePrompt);
          break;
        case 'odoo':
          response = await aiService.getOdooAssistance(servicePrompt);
          break;
        case 'sage':
          response = await aiService.getSageAssistance(servicePrompt);
          break;
        case 'gov-admin':
          response = await aiService.getGovernmentAssistance(servicePrompt);
          break;
        case 'togo-gov':
          response = await aiService.getTogoAssistance(servicePrompt);
          break;
        case 'gov-policy':
          response = await aiService.getPublicPolicyAssistance(servicePrompt);
          break;
        case 'gov-engagement':
          response = await aiService.getCitizenEngagementAssistance(servicePrompt);
          break;
        case 'gov-smart-city':
          response = await aiService.getSmartCityAssistance(servicePrompt);
          break;
        case 'gov-bias-detection':
          response = await aiService.getBiasDetectionAssistance(servicePrompt);
          break;
        case 'military':
          response = await aiService.getMilitaryAssistance(servicePrompt);
          break;
        case 'gendarmerie':
          response = await aiService.getGendarmerieAssistance(servicePrompt);
          break;
        case 'police':
          response = await aiService.getPoliceAssistance(servicePrompt);
          break;
        case 'security-opt':
          response = await aiService.getSecurityOptimization(servicePrompt);
          break;
        case 'cyber-sentinel':
          response = await aiService.getCybersecuritySentinel(servicePrompt);
          break;
        case 'conflict-debug':
          response = await aiService.debugCode(servicePrompt);
          break;
        case 'langflow':
          response = await aiService.executeLangflow(servicePrompt);
          break;
        case 'automl-feat':
          response = await aiService.getAutoMLFeatureEngineering(servicePrompt);
          break;
        case 'automl-tune':
          response = await aiService.getAutoMLHyperparameterTuning(servicePrompt);
          break;
        case 'automl-select':
          response = await aiService.getAutoMLModelSelection(servicePrompt);
          break;
        case 'automl-mlops':
          response = await aiService.getAutoMLMLOps(servicePrompt);
          break;
        case 'monetization':
          response = await aiService.getMonetizationAdvice(servicePrompt);
          break;
        case 'partnership':
          response = await aiService.getPartnershipAdvice(servicePrompt);
          break;
        case 'fundraising':
          response = await aiService.getFundraisingAdvice(servicePrompt);
          break;
        case 'llama-intel':
          response = await aiService.getLlamaIntelligence(servicePrompt);
          break;
        case 'llama-guard':
          response = await aiService.getLlamaGuard(servicePrompt);
          break;
        case 'nemotron':
          response = await aiService.getNemotronReasoning(servicePrompt);
          break;
        case 'mixtral':
          response = await aiService.getMixtralMultilingual(servicePrompt);
          break;
        case 'claude-intel':
          response = await aiService.getClaudeIntelligence(servicePrompt);
          break;
        case 'claude-coder':
          response = await aiService.getClaudeCoding(servicePrompt);
          break;
        case 'github-models':
          response = await aiService.getGitHubModelsAssistance(servicePrompt, executionParams.model_name);
          break;
        case 'copilot-chat':
          response = await aiService.getGitHubCopilotChat(servicePrompt);
          break;
        case 'copilot-coding':
          response = await aiService.getGitHubCopilotCoding(servicePrompt);
          break;
        default:
          // Fallback for demo purposes if specific endpoint isn't mapped in aiService yet
          response = { data: { message: "This service is currently in demo mode. The full integration is coming soon!" } };
      }
      }
      setServiceResponse(response.data.message || response.data.promotion_text || response.data.content || "Service executed successfully.");
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to execute service');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      setError(null);
      if (modalMode === 'register') {
        if (!username) return;
        const response = await userService.register(username);
        const { api_key } = response.data;
        localStorage.setItem('globalApiKey', api_key);
        setAuthToken(api_key);
        alert(`Your API Key is: ${api_key}. Please save it to login later!`);
      } else {
        if (!apiKey) return;
        const response = await userService.login(apiKey);
        const { api_key } = response.data;
        localStorage.setItem('globalApiKey', api_key);
        setAuthToken(api_key);
      }
      await fetchUserData();
      setShowLoginModal(false);
      setUsername('');
      setApiKey('');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsCameraActive(true);
      }
    } catch (err) {
      setError('Failed to access camera');
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = (videoRef.current.srcObject as MediaStream).getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
      setIsCameraActive(false);
    }
  };

  const capturePhoto = () => {
    if (videoRef.current) {
      const canvas = document.createElement('canvas');
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(videoRef.current, 0, 0);
        const dataUrl = canvas.toDataURL('image/jpeg');
        setCapturedMedia({ data: dataUrl, type: 'image/jpeg' });
        stopCamera();
      }
    }
  };

  const startRecording = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'video/webm' });
        const reader = new FileReader();
        reader.onloadend = () => {
          setCapturedMedia({ data: reader.result as string, type: 'video/webm' });
        };
        reader.readAsDataURL(blob);
        stopCamera();
      };

      mediaRecorder.start();
      setIsRecording(true);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const filteredServices = AI_SERVICES.filter(service => {
    const matchesSearch = service.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         service.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         service.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || service.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const filteredStoreAgents = storeAgents.filter(agent => {
    const matchesSearch = agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         agent.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         agent.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || agent.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const filteredStoreDesigns = storeDesigns.filter(design => {
    const matchesSearch = design.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         design.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         design.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'All' || design.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      {/* Navigation */}
      <nav className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex items-center space-x-2">
                <img src="/logo.svg" alt="Yendoukoa AI Logo" className="h-10 w-10" />
                <span className="text-2xl font-bold text-blue-600">Yendoukoa AI</span>
              </div>
              <div className="hidden md:ml-6 md:flex md:space-x-8">
                <button
                  onClick={() => setActiveTab('marketplace')}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'marketplace' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}
                >
                  Official Services
                </button>
                <button
                  onClick={() => setActiveTab('agents-store')}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'agents-store' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}
                >
                  AI Agents Store
                </button>
                <button
                  onClick={() => setActiveTab('design-store')}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'design-store' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}
                >
                  Design & API Store
                </button>
                <button
                  onClick={() => setActiveTab('dashboard')}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'dashboard' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}
                >
                  Dashboard
                </button>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              {user ? (
                <div className="flex items-center space-x-4">
                  <div className="flex items-center bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm font-semibold">
                    <CreditCard size={16} className="mr-2" />
                    {credits} Credits
                  </div>
                  <span className="text-sm font-medium text-gray-700">{user.username}</span>
                  <button className="text-gray-500 hover:text-gray-700" onClick={() => {
                    localStorage.removeItem('globalApiKey');
                    setAuthToken(null);
                    setUser(null);
                  }}>
                    <X size={20} />
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setShowLoginModal(true)}
                  disabled={loading}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700"
                >
                  {loading ? 'Connecting...' : 'Login / Register'}
                </button>
              )}
              <button className="md:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
                {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 mx-auto max-w-7xl mt-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <AlertCircle className="h-5 w-5 text-red-400" />
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Service Execution Modal */}
      {showServiceModal && selectedService && (
        <div className="fixed inset-0 z-[60] overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true" onClick={() => setShowServiceModal(false)}>
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div className="relative inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full z-[70]">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div className="sm:flex sm:items-start">
                  <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 sm:mx-0 sm:h-10 sm:w-10">
                    <selectedService.icon className="h-6 w-6 text-blue-600" />
                  </div>
                  <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">
                      Use {selectedService.name}
                    </h3>
                    <div className="mt-4">
                      {!serviceResponse ? (
                        <form onSubmit={handleServiceExecution}>
                          {selectedService.id === 'marketing' && (
                            <div className="mb-4 bg-gray-50 p-4 rounded-lg border">
                              <label className="block text-sm font-medium text-gray-700 mb-2">Select Marketing Service</label>
                              <div className="flex space-x-4">
                                <label className="inline-flex items-center">
                                  <input
                                    type="radio"
                                    className="form-radio"
                                    name="marketingType"
                                    value="bot"
                                    checked={executionParams.type !== 'video'}
                                    onChange={() => setExecutionParams({ ...executionParams, type: 'bot' })}
                                  />
                                  <span className="ml-2 text-sm">Bot & Strategy</span>
                                </label>
                                <label className="inline-flex items-center">
                                  <input
                                    type="radio"
                                    className="form-radio"
                                    name="marketingType"
                                    value="video"
                                    checked={executionParams.type === 'video'}
                                    onChange={() => setExecutionParams({ ...executionParams, type: 'video' })}
                                  />
                                  <span className="ml-2 text-sm">Veo Video Gen</span>
                                </label>
                              </div>
                            </div>
                          )}
                          {(selectedService.id === 'visual-intel' || selectedService.category === 'Advanced') && (
                            <div className="mb-4">
                              <label className="block text-sm font-medium text-gray-700 mb-2">Multimodal Input (Optional for Advanced Agents)</label>
                              <div className="border-2 border-dashed rounded-lg p-4 flex flex-col items-center justify-center bg-gray-50">
                                {isCameraActive ? (
                                  <div className="w-full flex flex-col items-center">
                                    <video ref={videoRef} autoPlay playsInline className="w-full max-w-sm rounded-lg mb-2" />
                                    <div className="flex space-x-2">
                                      {!isRecording ? (
                                        <>
                                          <button
                                            type="button"
                                            onClick={capturePhoto}
                                            className="bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700"
                                            title="Take Photo"
                                          >
                                            <Camera size={20} />
                                          </button>
                                          <button
                                            type="button"
                                            onClick={startRecording}
                                            className="bg-red-600 text-white p-2 rounded-full hover:bg-red-700"
                                            title="Start Recording"
                                          >
                                            <Video size={20} />
                                          </button>
                                        </>
                                      ) : (
                                        <button
                                          type="button"
                                          onClick={stopRecording}
                                          className="bg-gray-800 text-white p-2 rounded-full hover:bg-black animate-pulse"
                                          title="Stop Recording"
                                        >
                                          <div className="w-5 h-5 bg-red-600 rounded-sm"></div>
                                        </button>
                                      )}
                                      <button
                                        type="button"
                                        onClick={stopCamera}
                                        className="bg-gray-400 text-white p-2 rounded-full hover:bg-gray-500"
                                      >
                                        <X size={20} />
                                      </button>
                                    </div>
                                  </div>
                                ) : capturedMedia ? (
                                  <div className="w-full flex flex-col items-center">
                                    {capturedMedia.type.startsWith('image') ? (
                                      <img src={capturedMedia.data} alt="Captured" className="w-full max-w-sm rounded-lg mb-2" />
                                    ) : (
                                      <video src={capturedMedia.data} controls className="w-full max-w-sm rounded-lg mb-2" />
                                    )}
                                    <button
                                      type="button"
                                      onClick={() => { setCapturedMedia(null); startCamera(); }}
                                      className="text-blue-600 text-sm font-medium hover:underline"
                                    >
                                      Retake
                                    </button>
                                  </div>
                                ) : (
                                  <button
                                    type="button"
                                    onClick={startCamera}
                                    className="flex flex-col items-center text-gray-500 hover:text-blue-600"
                                  >
                                    <Camera size={40} />
                                    <span className="mt-2 text-sm">Open Camera</span>
                                  </button>
                                )}
                              </div>
                            </div>
                          )}
                          {['gumloop', 'n8n', 'lamatic'].includes(selectedService.id) && (
                            <div className="mb-4 bg-gray-50 p-4 rounded-lg border">
                              <div className="flex items-center mb-4">
                                <input
                                  type="checkbox"
                                  id="execute-workflow"
                                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                                  checked={executionParams.execute || false}
                                  onChange={(e) => setExecutionParams({ ...executionParams, execute: e.target.checked })}
                                />
                                <label htmlFor="execute-workflow" className="ml-2 block text-sm text-gray-900 font-medium">
                                  Trigger Workflow / Execute Action
                                </label>
                              </div>

                              {executionParams.execute && (
                                <div className="space-y-4">
                                  {selectedService.id === 'gumloop' && (
                                    <div>
                                      <label className="block text-sm font-medium text-gray-700">Pipeline ID</label>
                                      <input
                                        type="text"
                                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                                        placeholder="Enter Gumloop Pipeline ID"
                                        value={executionParams.pipeline_id || ''}
                                        onChange={(e) => setExecutionParams({ ...executionParams, pipeline_id: e.target.value })}
                                        required
                                      />
                                    </div>
                                  )}
                                  {selectedService.id === 'n8n' && (
                                    <div>
                                      <label className="block text-sm font-medium text-gray-700">Webhook URL (Optional if using default)</label>
                                      <input
                                        type="text"
                                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                                        placeholder="https://your-n8n-instance.com/webhook/..."
                                        value={executionParams.webhook_url || ''}
                                        onChange={(e) => setExecutionParams({ ...executionParams, webhook_url: e.target.value })}
                                      />
                                    </div>
                                  )}
                                  {selectedService.id === 'github-models' && (
                                    <div>
                                      <label className="block text-sm font-medium text-gray-700">Model Name</label>
                                      <select
                                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                                        value={executionParams.model_name || 'gpt-4o'}
                                        onChange={(e) => setExecutionParams({ ...executionParams, model_name: e.target.value })}
                                      >
                                        <option value="gpt-4o">GPT-4o</option>
                                        <option value="Llama-3.1-405b-Instruct">Llama 3.1 405B</option>
                                        <option value="Phi-3.5-moe-instruct">Phi 3.5 MoE</option>
                                        <option value="Mistral-Large-2407">Mistral Large</option>
                                      </select>
                                    </div>
                                  )}
                                  {selectedService.id === 'lamatic' && (
                                    <div>
                                      <label className="block text-sm font-medium text-gray-700">Workflow ID</label>
                                      <input
                                        type="text"
                                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                                        placeholder="Enter Lamatic.ai Workflow ID"
                                        value={executionParams.workflow_id || ''}
                                        onChange={(e) => setExecutionParams({ ...executionParams, workflow_id: e.target.value })}
                                        required
                                      />
                                    </div>
                                  )}
                                </div>
                              )}
                            </div>
                          )}
                          <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700">Prompt / Requirements</label>
                            <textarea
                              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                              placeholder={`Describe what you need the ${selectedService.name} to do...`}
                              value={servicePrompt}
                              onChange={(e) => setServicePrompt(e.target.value)}
                              rows={5}
                              required={!executionParams.execute}
                            />
                          </div>
                          <div className="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
                            <button
                              type="submit"
                              disabled={loading}
                              className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
                            >
                              {loading ? 'Processing...' : 'Run Service (50 Credits)'}
                            </button>
                            <button
                              type="button"
                              onClick={() => {
                                stopCamera();
                                setShowServiceModal(false);
                              }}
                              className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:w-auto sm:text-sm"
                            >
                              Cancel
                            </button>
                          </div>
                        </form>
                      ) : (
                        <div className="space-y-4">
                          <div className="bg-gray-50 p-4 rounded-lg border max-h-[400px] overflow-y-auto">
                            <p className="text-sm text-gray-700 whitespace-pre-wrap">{serviceResponse}</p>
                          </div>
                          <div className="flex justify-end">
                             <button
                               onClick={() => setServiceResponse('')}
                               className="mr-3 inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 text-sm"
                             >
                               Try Again
                             </button>
                             <button
                               onClick={handleSaveToStorage}
                               disabled={loading}
                               className="mr-3 inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 text-sm"
                             >
                               <Save size={16} className="mr-2" />
                               {loading ? 'Saving...' : 'Save to Storage'}
                             </button>
                             <button
                               onClick={() => setShowServiceModal(false)}
                               className="inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 text-sm"
                             >
                               Done
                             </button>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Agent Registration Modal */}
      {showAgentRegModal && (
        <div className="fixed inset-0 z-[60] overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true" onClick={() => setShowAgentRegModal(false)}>
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div className="relative inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full z-[70]">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">Register New AI Agent</h3>
                <form onSubmit={handleAgentRegistration} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Agent Name</label>
                    <input
                      type="text"
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                      value={newAgent.name}
                      onChange={(e) => setNewAgent({...newAgent, name: e.target.value})}
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Description</label>
                    <textarea
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                      value={newAgent.description}
                      onChange={(e) => setNewAgent({...newAgent, description: e.target.value})}
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Endpoint URL</label>
                    <input
                      type="url"
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                      placeholder="https://your-agent-api.com/execute"
                      value={newAgent.endpoint_url}
                      onChange={(e) => setNewAgent({...newAgent, endpoint_url: e.target.value})}
                      required
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Price (Credits)</label>
                      <input
                        type="number"
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                        value={newAgent.price_per_use}
                        onChange={(e) => setNewAgent({...newAgent, price_per_use: parseInt(e.target.value)})}
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Category</label>
                      <select
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                        value={newAgent.category}
                        onChange={(e) => setNewAgent({...newAgent, category: e.target.value})}
                      >
                        <option value="General">General</option>
                        <option value="Development">Development</option>
                        <option value="Business">Business</option>
                        <option value="Security">Security</option>
                      </select>
                    </div>
                  </div>
                  <div className="mt-5 sm:mt-6 sm:flex sm:flex-row-reverse">
                    <button type="submit" disabled={loading} className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 sm:ml-3 sm:w-auto sm:text-sm">
                      {loading ? 'Submitting...' : 'Register Agent'}
                    </button>
                    <button type="button" onClick={() => setShowAgentRegModal(false)} className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:w-auto sm:text-sm">
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Design Registration Modal */}
      {showDesignRegModal && (
        <div className="fixed inset-0 z-[60] overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true" onClick={() => setShowDesignRegModal(false)}>
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div className="relative inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full z-[70]">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">List New Design / API</h3>
                <form onSubmit={handleDesignRegistration} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Design Name</label>
                    <input
                      type="text"
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                      value={newDesign.name}
                      onChange={(e) => setNewDesign({...newDesign, name: e.target.value})}
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Description</label>
                    <textarea
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                      value={newDesign.description}
                      onChange={(e) => setNewDesign({...newDesign, description: e.target.value})}
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700">Content (Code or JSON)</label>
                    <textarea
                      className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm font-mono"
                      rows={5}
                      value={newDesign.content}
                      onChange={(e) => setNewDesign({...newDesign, content: e.target.value})}
                      required
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Price (Credits)</label>
                      <input
                        type="number"
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                        value={newDesign.price}
                        onChange={(e) => setNewDesign({...newDesign, price: parseInt(e.target.value)})}
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Category</label>
                      <select
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 sm:text-sm"
                        value={newDesign.category}
                        onChange={(e) => setNewDesign({...newDesign, category: e.target.value})}
                      >
                        <option value="Web">Web</option>
                        <option value="Mobile">Mobile</option>
                        <option value="API">API</option>
                        <option value="Landing Page">Landing Page</option>
                      </select>
                    </div>
                  </div>
                  <div className="mt-5 sm:mt-6 sm:flex sm:flex-row-reverse">
                    <button type="submit" disabled={loading} className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-purple-600 text-base font-medium text-white hover:bg-purple-700 sm:ml-3 sm:w-auto sm:text-sm">
                      {loading ? 'Submitting...' : 'List Design'}
                    </button>
                    <button type="button" onClick={() => setShowDesignRegModal(false)} className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:w-auto sm:text-sm">
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Login Modal */}
      {showLoginModal && (
        <div className="fixed inset-0 z-[60] overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true" onClick={() => setShowLoginModal(false)}>
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div className="relative inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full z-[70]">
              <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <div className="sm:flex sm:items-start">
                  <div className="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 sm:mx-0 sm:h-10 sm:w-10">
                    {modalMode === 'register' ? <UserIcon className="h-6 w-6 text-blue-600" /> : <Key className="h-6 w-6 text-blue-600" />}
                  </div>
                  <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">
                      {modalMode === 'register' ? 'Join Yendoukoa AI' : 'Login with API Key'}
                    </h3>
                    <div className="mt-4">
                      <form onSubmit={handleSubmit}>
                        {modalMode === 'register' ? (
                          <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700">Username</label>
                            <input
                              type="text"
                              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                              placeholder="Choose a username"
                              value={username}
                              onChange={(e) => setUsername(e.target.value)}
                              required
                            />
                          </div>
                        ) : (
                          <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700">API Key</label>
                            <input
                              type="password"
                              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                              placeholder="Enter your API Key"
                              value={apiKey}
                              onChange={(e) => setApiKey(e.target.value)}
                              required
                            />
                          </div>
                        )}
                        <div className="mt-4 flex justify-center text-sm">
                           <button
                             type="button"
                             onClick={() => setModalMode(modalMode === 'register' ? 'login' : 'register')}
                             className="text-blue-600 hover:underline"
                           >
                             {modalMode === 'register' ? 'Already have an API Key? Login' : 'Need an account? Register'}
                           </button>
                        </div>
                        <div className="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
                          <button
                            type="submit"
                            disabled={loading}
                            className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
                          >
                            {loading ? 'Processing...' : modalMode === 'register' ? 'Register' : 'Login'}
                          </button>
                          <button
                            type="button"
                            onClick={() => setShowLoginModal(false)}
                            className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:w-auto sm:text-sm"
                          >
                            Cancel
                          </button>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* LangChain/Langflow Badge */}
      <div className="bg-blue-700 text-white py-2">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-center items-center space-x-4 text-xs font-semibold">
           <span className="bg-blue-500 px-2 py-1 rounded">Powered by LangChain</span>
           <span className="bg-green-500 px-2 py-1 rounded">Enhanced with Langflow</span>
        </div>
      </div>

      {/* Hero Section */}
      <div className="bg-blue-600 text-white py-20 relative overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[1000px] bg-blue-500 rounded-full blur-[120px] opacity-20 -z-10"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center">
            <h1 className="text-5xl font-black tracking-tighter sm:text-6xl lg:text-7xl">
              Explore the Future of <span className="text-blue-200">Intelligence</span>
            </h1>
            <p className="mt-8 text-xl text-blue-100 max-w-2xl mx-auto font-medium leading-relaxed">
              Yendoukoa AI provides an elite marketplace of specialized agents. Explore our ecosystem to find the perfect autonomous partner for your project.
            </p>
            <div className="mt-12 max-w-2xl mx-auto">
              <div className="relative group">
                <div className="absolute -inset-1 bg-gradient-to-r from-blue-400 to-indigo-400 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
                <div className="relative flex items-center">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <Search className="h-6 w-6 text-blue-600" />
                  </div>
                  <input
                    type="text"
                    className="block w-full pl-12 pr-4 py-5 border-none rounded-2xl leading-5 bg-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-4 focus:ring-blue-400/50 shadow-2xl text-lg font-bold"
                    placeholder="Search for agents, roles, or domains..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                  <div className="absolute right-3">
                    <button className="bg-blue-600 text-white px-6 py-3 rounded-xl font-black text-sm hover:bg-blue-700 transition-colors">
                      Search
                    </button>
                  </div>
                </div>
              </div>
              <div className="mt-6 flex flex-wrap justify-center gap-3">
                <span className="text-blue-200 text-sm font-bold self-center mr-2 uppercase tracking-widest">Trending:</span>
                {['Security', 'Development', 'National Security', 'USSD'].map(tag => (
                  <button
                    key={tag}
                    onClick={() => setSearchQuery(tag)}
                    className="bg-blue-700/50 hover:bg-blue-500 text-white px-4 py-1.5 rounded-full text-xs font-black transition-all border border-blue-400/30"
                  >
                    #{tag}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {activeTab === 'marketplace' ? (
          <div>
            {/* Featured Agents Section */}
            {selectedCategory === 'All' && !searchQuery && (
              <div className="mb-16">
                <div className="flex items-center justify-between mb-8">
                  <div>
                    <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">Our Core AI Specialists</h2>
                    <p className="mt-2 text-lg text-gray-500">Experience the primary intelligence pillars of the Yendoukoa ecosystem.</p>
                  </div>
                  <div className="hidden sm:flex items-center text-blue-600 font-semibold cursor-pointer hover:underline">
                    Explore all <TrendingUp size={20} className="ml-1" />
                  </div>
                </div>
                <div className="grid grid-cols-1 gap-y-10 gap-x-6 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
                  {AI_SERVICES.filter(s => s.featured).map((service) => (
                    <div key={service.id} className="group relative bg-white border-2 border-blue-600 rounded-2xl overflow-hidden shadow-xl transform transition-all hover:scale-105 hover:shadow-2xl">
                      <div className="p-8">
                        <div className="flex items-center justify-between mb-6">
                          <div className="p-4 bg-blue-600 rounded-2xl text-white">
                            <service.icon size={32} />
                          </div>
                          <div className="flex items-center bg-blue-100 text-blue-700 px-2 py-1 rounded-md text-[10px] font-black uppercase tracking-tighter">
                            <Zap size={10} className="mr-1 fill-current" /> Main Role
                          </div>
                        </div>
                        <h3 className="text-xl font-black text-gray-900 mb-2 tracking-tight">
                          {service.name}
                        </h3>
                        <p className="text-gray-500 text-sm line-clamp-3 mb-8 font-medium leading-relaxed">
                          {service.description}
                        </p>
                        <button
                          onClick={() => {
                            setSelectedService(service);
                            setShowServiceModal(true);
                            setServicePrompt('');
                            setServiceResponse('');
                            setExecutionParams({});
                          }}
                          className="w-full bg-blue-600 text-white py-3 rounded-xl text-sm font-black hover:bg-blue-700 transition-colors shadow-lg"
                        >
                          Launch Agent
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Explore Features Section */}
            {selectedCategory === 'All' && !searchQuery && (
              <div className="mb-16 bg-gray-900 rounded-3xl p-8 sm:p-12 text-white overflow-hidden relative">
                <div className="absolute top-0 right-0 -mt-20 -mr-20 w-64 h-64 bg-blue-500 rounded-full blur-[100px] opacity-20"></div>
                <div className="absolute bottom-0 left-0 -mb-20 -ml-20 w-64 h-64 bg-purple-500 rounded-full blur-[100px] opacity-20"></div>

                <div className="relative z-10">
                  <h2 className="text-3xl font-black mb-4">Explore our Ecosystem</h2>
                  <p className="text-gray-400 text-lg mb-10 max-w-2xl">Discover specialized AI tools across every domain. From high-fidelity video generation to national security and blockchain infrastructure.</p>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
                    {[
                      { name: 'Public Services', icon: Building2, count: 8, color: 'bg-emerald-500/10 text-emerald-500' },
                      { name: 'Development', icon: Code2, count: 12, color: 'bg-blue-500/10 text-blue-500' },
                      { name: 'National Security', icon: ShieldCheck, count: 6, color: 'bg-red-500/10 text-red-500' },
                      { name: 'Advanced AI', icon: Brain, count: 15, color: 'bg-purple-500/10 text-purple-500' },
                    ].map((item) => (
                      <div
                        key={item.name}
                        onClick={() => setSelectedCategory(item.name.includes('Dev') ? 'Development' : item.name.includes('Public') ? 'Public' : item.name.includes('Security') ? 'Security' : 'Advanced')}
                        className="bg-white/5 border border-white/10 p-6 rounded-2xl hover:bg-white/10 transition-all cursor-pointer group"
                      >
                        <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-4 ${item.color}`}>
                          <item.icon size={24} />
                        </div>
                        <h4 className="font-bold text-white group-hover:text-blue-400 transition-colors">{item.name}</h4>
                        <p className="text-gray-500 text-sm mt-1">{item.count}+ specialists</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 space-y-4 md:space-y-0">
              <div>
                <h2 className="text-2xl font-black text-gray-900 uppercase tracking-widest flex items-center">
                  <Layout className="mr-3 text-blue-600" /> Specialist Marketplace
                </h2>
                {selectedCategory !== 'All' && (
                   <p className="text-blue-600 font-bold mt-1">Showing {selectedCategory} Specialists</p>
                )}
              </div>
              <div className="flex space-x-2 overflow-x-auto pb-2 w-full md:w-auto no-scrollbar">
                {['All', 'Development', 'Business', 'Public', 'Support', 'Security', 'Advanced', 'Infrastructure', 'Science', 'Arts'].map(cat => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`whitespace-nowrap px-6 py-2.5 rounded-xl border-2 text-sm font-black transition-all ${
                      selectedCategory === cat
                        ? 'bg-blue-600 text-white border-blue-600 shadow-lg shadow-blue-200'
                        : 'bg-white text-gray-500 border-gray-100 hover:border-blue-200 hover:text-blue-600'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 gap-y-8 gap-x-6 sm:grid-cols-2 lg:grid-cols-3 xl:gap-x-8">
              {filteredServices.map((service) => (
                <div key={service.id} className="group bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                  <div className="p-8">
                    <div className="flex items-center justify-between mb-6">
                      <div className="p-3 bg-gray-50 rounded-xl text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors duration-300">
                        <service.icon size={24} />
                      </div>
                      <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest bg-gray-50 px-2 py-1 rounded">
                        {service.category}
                      </span>
                    </div>
                    <h3 className="text-lg font-black text-gray-900 group-hover:text-blue-600 transition-colors">
                      {service.name}
                    </h3>
                    <p className="mt-3 text-sm text-gray-500 line-clamp-2 leading-relaxed">
                      {service.description}
                    </p>
                    <div className="mt-8 pt-6 border-t border-gray-50 flex items-center justify-between">
                      <div className="flex items-center text-blue-600">
                         <CreditCard size={14} className="mr-1.5" />
                         <span className="text-sm font-black">50 Credits</span>
                      </div>
                      <button
                        onClick={() => {
                          setSelectedService(service);
                          setShowServiceModal(true);
                          setServicePrompt('');
                          setServiceResponse('');
                          setExecutionParams({});
                        }}
                        className="bg-gray-900 text-white px-5 py-2.5 rounded-xl text-xs font-black hover:bg-blue-600 transition-all shadow-md active:scale-95"
                      >
                        Deploy Agent
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : activeTab === 'agents-store' ? (
          <div className="space-y-12">
            <div className="bg-gradient-to-r from-blue-900 to-indigo-900 rounded-3xl p-8 text-white">
              <div className="flex flex-col md:flex-row justify-between items-center">
                <div className="max-w-xl">
                  <h2 className="text-3xl font-black mb-4 uppercase tracking-tight">AI Agents Store</h2>
                  <p className="text-blue-100 text-lg font-medium opacity-80">
                    Discover and deploy specialized AI agents built by our global developer community.
                    Developers earn 80% revenue on every execution.
                  </p>
                </div>
                <button
                  onClick={() => {
                    if (!user) setShowLoginModal(true);
                    else {
                      setShowAgentRegModal(true);
                    }
                  }}
                  className="mt-6 md:mt-0 bg-white text-blue-900 px-8 py-4 rounded-2xl font-black text-sm hover:bg-blue-50 transition-colors shadow-2xl"
                >
                  Submit Your Agent
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-y-8 gap-x-6 sm:grid-cols-2 lg:grid-cols-3 xl:gap-x-8">
              {filteredStoreAgents.length === 0 ? (
                 <div className="col-span-full text-center py-20 text-gray-500">
                    <Bot size={64} className="mx-auto mb-4 opacity-10" />
                    <p className="text-xl font-bold">No community agents found yet.</p>
                    <p>Be the first to list your agent on the store!</p>
                 </div>
              ) : filteredStoreAgents.map((agent) => (
                <div key={agent.id} className="group bg-white border-2 border-gray-100 rounded-2xl overflow-hidden shadow-sm hover:border-blue-500 transition-all duration-300">
                  <div className="p-8">
                    <div className="flex items-center justify-between mb-6">
                      <div className="p-3 bg-blue-50 rounded-xl text-blue-600">
                        <Bot size={24} />
                      </div>
                      <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest bg-gray-50 px-2 py-1 rounded">
                        {agent.category}
                      </span>
                    </div>
                    <h3 className="text-lg font-black text-gray-900">
                      {agent.name}
                    </h3>
                    <p className="mt-1 text-xs text-blue-600 font-bold mb-3">by {agent.developer_name}</p>
                    <p className="text-sm text-gray-500 line-clamp-2 leading-relaxed">
                      {agent.description}
                    </p>
                    <div className="mt-8 pt-6 border-t border-gray-50 flex items-center justify-between">
                      <div className="flex items-center text-blue-600">
                         <CreditCard size={14} className="mr-1.5" />
                         <span className="text-sm font-black">{agent.price_per_use} Credits</span>
                      </div>
                      <button
                        onClick={() => {
                          setSelectedService({
                             id: agent.id,
                             name: agent.name,
                             description: agent.description,
                             category: agent.category,
                             icon: Bot,
                             isStoreItem: true,
                             type: 'agent'
                          });
                          setShowServiceModal(true);
                          setServicePrompt('');
                          setServiceResponse('');
                        }}
                        className="bg-blue-600 text-white px-5 py-2.5 rounded-xl text-xs font-black hover:bg-blue-700 transition-all shadow-md"
                      >
                        Launch Community Agent
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : activeTab === 'design-store' ? (
          <div className="space-y-12">
            <div className="bg-gradient-to-r from-purple-900 to-blue-900 rounded-3xl p-8 text-white">
              <div className="flex flex-col md:flex-row justify-between items-center">
                <div className="max-w-xl">
                  <h2 className="text-3xl font-black mb-4 uppercase tracking-tight">Design & API Store</h2>
                  <p className="text-blue-100 text-lg font-medium opacity-80">
                    Acquire elite UI/UX designs, landing pages, and specialized API configurations.
                    Instant download and ownership of high-quality digital assets.
                  </p>
                </div>
                <button
                  onClick={() => {
                    if (!user) setShowLoginModal(true);
                    else {
                      setShowDesignRegModal(true);
                    }
                  }}
                  className="mt-6 md:mt-0 bg-white text-purple-900 px-8 py-4 rounded-2xl font-black text-sm hover:bg-blue-50 transition-colors shadow-2xl"
                >
                  List Your Design
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-y-8 gap-x-6 sm:grid-cols-2 lg:grid-cols-3 xl:gap-x-8">
               {filteredStoreDesigns.length === 0 ? (
                 <div className="col-span-full text-center py-20 text-gray-500">
                    <Layout size={64} className="mx-auto mb-4 opacity-10" />
                    <p className="text-xl font-bold">The design vault is currently empty.</p>
                    <p>Developers, start listing your premium designs today!</p>
                 </div>
               ) : filteredStoreDesigns.map((design) => (
                <div key={design.id} className="group bg-white border border-gray-100 rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300">
                   <div className="aspect-video bg-gray-100 relative">
                      {design.preview_url ? (
                         <img src={design.preview_url} alt={design.name} className="w-full h-full object-cover" />
                      ) : (
                         <div className="w-full h-full flex items-center justify-center text-gray-300">
                            <Layout size={48} />
                         </div>
                      )}
                      <div className="absolute top-4 right-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-xs font-black text-purple-600">
                         {design.category}
                      </div>
                   </div>
                   <div className="p-8">
                    <h3 className="text-lg font-black text-gray-900 mb-1">{design.name}</h3>
                    <p className="text-xs text-purple-600 font-bold mb-4">by {design.developer_name}</p>
                    <p className="text-sm text-gray-500 line-clamp-2 mb-8 leading-relaxed">
                      {design.description}
                    </p>
                    <div className="flex items-center justify-between">
                       <div className="text-lg font-black text-gray-900">
                          {design.price} <span className="text-xs text-gray-400">Credits</span>
                       </div>
                       <button
                         onClick={() => {
                            setSelectedService({
                               id: design.id,
                               name: design.name,
                               description: design.description,
                               category: design.category,
                               icon: Layout,
                               isStoreItem: true,
                               type: 'design',
                               price: design.price
                            });
                            setShowServiceModal(true);
                            setServicePrompt('Purchase Confirmation');
                            setServiceResponse('');
                         }}
                         className="bg-purple-600 text-white px-6 py-2.5 rounded-xl text-xs font-black hover:bg-purple-700 transition-all shadow-lg"
                       >
                         Purchase & Access
                       </button>
                    </div>
                   </div>
                </div>
               ))}
            </div>
          </div>
        ) : (
          <div className="space-y-8">
             <div className="bg-white p-8 rounded-xl shadow-sm border">
                <h2 className="text-2xl font-bold mb-6">User Dashboard</h2>
                {!user ? (
                   <div className="text-center py-10">
                      <p className="text-gray-500 mb-4">Please login to view your dashboard</p>
                      <button onClick={() => setShowLoginModal(true)} className="text-blue-600 font-bold hover:underline">Login or Register Now</button>
                   </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="bg-blue-50 p-6 rounded-lg border border-blue-100">
                      <p className="text-blue-600 text-sm font-medium uppercase">Total Balance</p>
                      <p className="text-3xl font-bold mt-1 text-blue-900">{credits} Credits</p>
                    <p className="text-xs text-blue-400 mt-2 italic">* Official Balance from Database</p>
                    </div>
                    <div className="bg-green-50 p-6 rounded-lg border border-green-100">
                      <p className="text-green-600 text-sm font-medium uppercase">Active Projects</p>
                      <p className="text-3xl font-bold mt-1 text-green-900">3</p>
                    </div>
                    <div className="bg-purple-50 p-6 rounded-lg border border-purple-100">
                      <p className="text-purple-600 text-sm font-medium uppercase">Developer Earnings</p>
                      <p className="text-3xl font-bold mt-1 text-purple-900">
                         {Math.round(credits * 0.1)} <span className="text-sm font-medium">Credits</span>
                      </p>
                      <p className="text-[10px] text-purple-400 mt-2">Earned from community store sales</p>
                    </div>
                  </div>
                )}
             </div>

             {user && (
               <div className="bg-white p-8 rounded-xl shadow-sm border">
                 <h3 className="text-xl font-bold mb-6">Subscription Plan</h3>
                 <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                   <div className="border rounded-lg p-6 flex flex-col justify-between">
                     <div>
                       <h4 className="text-lg font-bold text-gray-900">Current Status</h4>
                       <div className="mt-2 flex items-center">
                         <span className={`px-3 py-1 rounded-full text-sm font-semibold ${user.subscription_status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                           {user.subscription_status === 'active' ? 'Active' : 'Inactive'}
                         </span>
                         <span className="ml-3 text-gray-500 capitalize">{user.subscription_plan} Plan</span>
                       </div>
                     </div>
                     {user.subscription_status !== 'active' && (
                       <p className="mt-4 text-sm text-gray-500">Upgrade to a premium plan to unlock more AI features and credits.</p>
                     )}
                   </div>

                   <div className="space-y-4">
                     <button
                       onClick={async () => {
                         try {
                           setLoading(true);
                           const res = await paymentService.createSubscriptionCheckout('premium');
                           window.location.href = res.data.url;
                         } catch (err) {
                           setError('Failed to initiate checkout');
                         } finally {
                           setLoading(false);
                         }
                       }}
                       className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-blue-700 transition-colors"
                     >
                       Upgrade to Premium ($19/mo)
                     </button>
                     <button
                       onClick={async () => {
                         try {
                           setLoading(true);
                           const res = await paymentService.createSubscriptionCheckout('pro');
                           window.location.href = res.data.url;
                         } catch (err) {
                           setError('Failed to initiate checkout');
                         } finally {
                           setLoading(false);
                         }
                       }}
                       className="w-full bg-gray-900 text-white px-6 py-3 rounded-lg font-bold hover:bg-black transition-colors"
                     >
                       Upgrade to Pro ($49/mo)
                     </button>
                   </div>
                 </div>
               </div>
             )}

             {user && (
               <>
                 <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div className="px-6 py-4 border-b flex justify-between items-center">
                      <h3 className="text-lg font-bold">File Storage Specialist</h3>
                      <label className="cursor-pointer bg-blue-600 text-white px-3 py-1 rounded-lg text-sm font-semibold hover:bg-blue-700">
                        <Plus size={16} className="inline mr-1" />
                        Upload File
                        <input type="file" className="hidden" onChange={handleFileUpload} />
                      </label>
                    </div>
                    <div className="p-6">
                      {userFiles.length === 0 ? (
                        <div className="text-center py-10 text-gray-500">
                          <Database size={48} className="mx-auto mb-4 opacity-20" />
                          <p>No files in storage yet. Generate content from AI services or upload files.</p>
                        </div>
                      ) : (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                          {userFiles.map((file) => (
                            <div key={file.id} className="p-4 border rounded-lg bg-gray-50 flex items-start justify-between">
                              <div className="flex items-start">
                                <FileText className="h-8 w-8 text-blue-600 mr-3 flex-shrink-0" />
                                <div className="min-w-0">
                                  <p className="font-bold text-sm truncate" title={file.filename}>{file.filename}</p>
                                  <p className="text-xs text-gray-500">{file.file_type}</p>
                                  <p className="text-[10px] text-gray-400 mt-1">{new Date(file.created_at).toLocaleDateString()}</p>
                                </div>
                              </div>
                              <div className="flex space-x-1">
                                <a
                                  href={`${import.meta.env.VITE_API_BASE_URL || '/api/v1'}/files/${file.id}?api_key=${localStorage.getItem('globalApiKey')}&download=true`}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="p-1 text-gray-400 hover:text-blue-600"
                                  title="Download"
                                >
                                  <Download size={16} />
                                </a>
                                <button
                                  onClick={() => handleDeleteFile(file.id)}
                                  className="p-1 text-gray-400 hover:text-red-600"
                                  title="Delete"
                                >
                                  <Trash2 size={16} />
                                </button>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                 </div>

                 <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div className="px-6 py-4 border-b">
                      <h3 className="text-lg font-bold">Integrated Tools</h3>
                    </div>
                    <div className="p-6">
                      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                        {AI_SERVICES.slice(0, 3).map((tool) => (
                           <div key={tool.id} className="flex items-center p-4 border rounded-lg bg-gray-50">
                              <tool.icon className="h-8 w-8 text-blue-600 mr-3" />
                              <div>
                                <p className="font-bold text-sm">{tool.name}</p>
                                <p className="text-xs text-green-600 font-medium">Integrated</p>
                              </div>
                           </div>
                        ))}
                        <button className="flex items-center justify-center p-4 border-2 border-dashed rounded-lg text-gray-400 hover:text-blue-600 hover:border-blue-600 transition-colors">
                           <span className="text-sm font-bold">+ Add New Tool</span>
                        </button>
                      </div>
                    </div>
                 </div>

                 <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
                    <div className="px-6 py-4 border-b">
                      <h3 className="text-lg font-bold">Recent Activity</h3>
                    </div>
                    <ul className="divide-y divide-gray-200">
                      {[
                        { id: 1, type: 'Website Gen', date: '2 hours ago', status: 'Completed', cost: '-50' },
                        { id: 2, type: 'Credit Top-up', date: 'Yesterday', status: 'Success', cost: '+1000' },
                        { id: 3, type: 'Legal Review', date: '2 days ago', status: 'Completed', cost: '-50' },
                      ].map((item) => (
                        <li key={item.id} className="px-6 py-4 flex items-center justify-between">
                          <div>
                            <p className="text-sm font-bold text-gray-900">{item.type}</p>
                            <p className="text-xs text-gray-500">{item.date}</p>
                          </div>
                          <div className="text-right">
                            <p className={`text-sm font-bold ${item.cost.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                              {item.cost}
                            </p>
                            <p className="text-xs text-gray-500">{item.status}</p>
                          </div>
                        </li>
                      ))}
                    </ul>
                 </div>
               </>
             )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="md:col-span-2">
              <div className="flex items-center space-x-2">
                <img src="/logo.svg" alt="Yendoukoa AI Logo" className="h-8 w-8" />
                <span className="text-2xl font-bold text-blue-600">Yendoukoa AI</span>
              </div>
              <p className="mt-4 text-gray-500 max-w-xs">
                Empowering businesses with professional-grade AI services and custom solutions.
              </p>
            </div>
            <div>
              <h4 className="font-bold mb-4 text-gray-900">Marketplace</h4>
              <ul className="space-y-2 text-sm text-gray-500">
                <li><a href="#" className="hover:text-blue-600">Development</a></li>
                <li><a href="#" className="hover:text-blue-600">Design</a></li>
                <li><a href="#" className="hover:text-blue-600">Business</a></li>
                <li><a href="#" className="hover:text-blue-600">Support</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4 text-gray-900">Resources</h4>
              <ul className="space-y-2 text-sm text-gray-500">
                <li><a href="./CHANGELOG.md" target="_blank" className="hover:text-blue-600">Changelog</a></li>
                <li><a href="#" className="hover:text-blue-600">Documentation</a></li>
                <li><a href="#" className="hover:text-blue-600">API Reference</a></li>
                <li><a href="#" className="hover:text-blue-600">Community</a></li>
                <li><a href="https://github.com/GYFX35/AI-services" className="hover:text-blue-600">GitHub</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t text-center text-sm text-gray-400">
            &copy; 2026 Yendoukoa AI. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
