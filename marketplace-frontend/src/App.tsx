import React, { useState, useEffect, useRef } from 'react';
import {
  Search, User as UserIcon, Zap, Wrench, ShieldCheck, Cpu, Globe, CreditCard,
  Menu, X, AlertCircle, Key, Gamepad2, Database, Code2, Scale, Stethoscope,
  Plane, Music, ShoppingBag, ShieldAlert, ShieldX, Binary, Bot, FlaskConical,
  Truck, Building2, BookOpen, Microscope, Layout, Mail, TrendingUp, Smartphone,
  Cloud, Server, DollarSign, Handshake, PiggyBank, Brain, Camera, Video,
  Settings, Route, Mic, FileText, Download, Trash2, Save, Plus, ArrowRight,
  Sparkles, CheckCircle2, ChevronRight, Play, ExternalLink, Loader2
} from 'lucide-react';
import { userService, aiService, paymentService, fileService, storeService, setAuthToken, type User, type File, type StoreAgent, type StoreDesign } from './api';
import type { AIService } from './types';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import ServiceCard from './components/ServiceCard';
import Footer from './components/Footer';
import Modal from './components/Modal';
import CategoryFilter from './components/CategoryFilter';
import Toast, { ToastType } from './components/Toast';

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

  // Theme State
  const [isDarkMode, setIsDarkMode] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('theme') === 'dark' ||
        (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    }
    return false;
  });

  // Toast State
  const [toast, setToast] = useState<{message: string, type: ToastType} | null>(null);

  const videoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    const savedApiKey = localStorage.getItem('globalApiKey');
    if (savedApiKey) {
      setAuthToken(savedApiKey);
      fetchUserData();
    }
    fetchStoreData();
  }, []);

  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [isDarkMode]);

  const toggleDarkMode = () => setIsDarkMode(!isDarkMode);

  const showToast = (message: string, type: ToastType = 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 5000);
  };

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
      fetchUserFiles();
    } catch (err) {
      console.error('Failed to fetch user data', err);
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

  const handleLogout = () => {
    localStorage.removeItem('globalApiKey');
    setAuthToken(null);
    setUser(null);
    setCredits(0);
    showToast('Logged out successfully', 'info');
  };

  const handleSaveToStorage = async () => {
    if (!serviceResponse || !selectedService) return;
    try {
      setLoading(true);
      const filename = `${selectedService.name.replace(/\s+/g, '_')}_${Date.now()}.txt`;
      await fileService.createDoc(filename, serviceResponse);
      showToast('Saved to vault successfully!', 'success');
      fetchUserFiles();
    } catch (err) {
      showToast('Failed to save to storage', 'error');
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
      showToast('File uploaded successfully', 'success');
      fetchUserFiles();
    } catch (err) {
      showToast('Failed to upload file', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteFile = async (id: number) => {
    if (!confirm('Are you sure you want to delete this file?')) return;
    try {
      setLoading(true);
      await fileService.deleteFile(id);
      showToast('File deleted', 'info');
      fetchUserFiles();
    } catch (err) {
      showToast('Failed to delete file', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleAgentRegistration = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      await storeService.registerAgent(newAgent);
      showToast('Agent registered successfully!', 'success');
      setShowAgentRegModal(false);
      fetchStoreData();
    } catch (err: any) {
      showToast(err.response?.data?.error || 'Failed to register agent', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDesignRegistration = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      await storeService.registerDesign(newDesign);
      showToast('Design listed successfully!', 'success');
      setShowDesignRegModal(false);
      fetchStoreData();
    } catch (err: any) {
      showToast(err.response?.data?.error || 'Failed to register design', 'error');
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
    if (!servicePrompt && !selectedService?.id) return;

    try {
      setLoading(true);
      let response;
      const mediaData = capturedMedia?.data.split(',')[1];
      const mimeType = capturedMedia?.type;

      if (selectedService?.isStoreItem) {
         if (selectedService.type === 'agent') {
            response = await storeService.executeAgent(selectedService.id as number, servicePrompt);
         } else {
            response = await storeService.purchaseDesign(selectedService.id as number);
         }
      } else {
      switch (selectedService?.id) {
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
          response = { data: { message: "This service is currently in demo mode. The full integration is coming soon!" } };
      }
      }
      setServiceResponse(response.data.message || response.data.promotion_text || response.data.content || "Service executed successfully.");
      showToast('Agent execution completed', 'success');
      fetchUserData(); // Refresh credits
    } catch (err: any) {
      showToast(err.response?.data?.error || 'Failed to execute service', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleAuthSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      if (modalMode === 'register') {
        if (!username) return;
        const response = await userService.register(username);
        const { api_key } = response.data;
        localStorage.setItem('globalApiKey', api_key);
        setAuthToken(api_key);
        showToast('Account created successfully!', 'success');
        alert(`Your API Key is: ${api_key}. Please save it to login later!`);
      } else {
        if (!apiKey) return;
        const response = await userService.login(apiKey);
        const { api_key } = response.data;
        localStorage.setItem('globalApiKey', api_key);
        setAuthToken(api_key);
        showToast('Logged in successfully', 'success');
      }
      await fetchUserData();
      setShowLoginModal(false);
      setUsername('');
      setApiKey('');
    } catch (err: any) {
      showToast(err.response?.data?.error || 'Authentication failed', 'error');
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
      showToast('Failed to access camera', 'error');
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
        showToast('Photo captured', 'info');
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
        showToast('Video recorded', 'info');
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

  const launchService = (service: AIService) => {
    setSelectedService(service);
    setShowServiceModal(true);
    setServicePrompt('');
    setServiceResponse('');
    setExecutionParams({});
    setCapturedMedia(null);
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
    <div className="min-h-screen bg-[#FDFDFD] text-gray-900 font-sans selection:bg-blue-100 selection:text-blue-600 dark:bg-[#0A0A0A] dark:text-gray-100 transition-colors duration-300">
      <Navbar
        user={user}
        credits={credits}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isMenuOpen={isMenuOpen}
        setIsMenuOpen={setIsMenuOpen}
        setShowLoginModal={setShowLoginModal}
        handleLogout={handleLogout}
        loading={loading}
        isDarkMode={isDarkMode}
        toggleDarkMode={toggleDarkMode}
      />

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      {/* Hero Section */}
      {activeTab === 'marketplace' && (
        <Hero
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          onTryAI={() => {
            const engineer = AI_SERVICES.find(s => s.id === 'website');
            if (engineer) launchService(engineer);
          }}
        />
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {activeTab === 'marketplace' && (
          <div className="space-y-24">
            {/* Featured Section */}
            {selectedCategory === 'All' && !searchQuery && (
              <section>
                <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 space-y-4">
                  <div className="max-w-2xl">
                    <h2 className="text-4xl font-black text-gray-900 dark:text-white tracking-tight mb-4 uppercase tracking-widest text-sm text-blue-600">
                      Core Intelligence
                    </h2>
                    <p className="text-2xl font-black text-gray-900 dark:text-white tracking-tight leading-tight">
                      Experience the primary pillars of the <span className="text-blue-600 underline decoration-blue-200 underline-offset-8">Yendoukoa ecosystem.</span>
                    </p>
                  </div>
                  <button className="flex items-center text-gray-900 dark:text-gray-300 font-black text-sm hover:text-blue-600 transition-colors group">
                    View all agents <ArrowRight size={16} className="ml-2 group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>
                <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
                  {AI_SERVICES.filter(s => s.featured).map((service) => (
                    <ServiceCard key={service.id} service={service} onLaunch={launchService} />
                  ))}
                </div>
              </section>
            )}

            {/* General Marketplace */}
            <section id="marketplace">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 space-y-6 md:space-y-0">
                <div>
                  <h2 className="text-3xl font-black text-gray-900 dark:text-white flex items-center tracking-tight">
                    <Sparkles className="mr-3 text-blue-600" /> Specialist Marketplace
                  </h2>
                  <p className="text-gray-500 dark:text-gray-400 font-bold mt-2">Browse {filteredServices.length} specialized AI assistants.</p>
                </div>
                <CategoryFilter
                  categories={['All', 'Development', 'Business', 'Public', 'Support', 'Security', 'Advanced', 'Infrastructure', 'Science', 'Arts']}
                  selectedCategory={selectedCategory}
                  onSelectCategory={setSelectedCategory}
                />
              </div>

              <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
                {filteredServices.map((service) => (
                  <ServiceCard key={service.id} service={service} onLaunch={launchService} />
                ))}
              </div>
            </section>
          </div>
        )}

        {activeTab === 'agents-store' && (
          <div className="space-y-16">
             <div className="bg-gray-900 rounded-[40px] p-12 text-white relative overflow-hidden">
                <div className="absolute top-0 right-0 w-96 h-96 bg-blue-600 rounded-full blur-[150px] opacity-20"></div>
                <div className="relative z-10 flex flex-col md:flex-row justify-between items-center gap-12">
                   <div className="max-w-2xl">
                      <h2 className="text-5xl font-black mb-6 tracking-tight">AI Agents Store</h2>
                      <p className="text-xl text-gray-400 font-medium leading-relaxed">
                        The decentralized hub for autonomous intelligence. Buy, sell, and deploy community-built agents with 80% revenue share for developers.
                      </p>
                      <div className="mt-10 flex items-center space-x-6">
                         <div className="flex -space-x-3">
                            {[1,2,3,4].map(i => (
                               <div key={i} className="w-10 h-10 rounded-full border-2 border-gray-900 bg-gray-800 flex items-center justify-center overflow-hidden">
                                  <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${i}`} alt="User" />
                               </div>
                            ))}
                         </div>
                         <p className="text-sm font-bold text-gray-400"><span className="text-white">1,200+</span> developers building today</p>
                      </div>
                   </div>
                   <div className="flex flex-col items-center bg-white/5 backdrop-blur-xl border border-white/10 p-8 rounded-[32px] w-full md:w-auto">
                      <button
                        onClick={() => { if(!user) setShowLoginModal(true); else setShowAgentRegModal(true); }}
                        className="w-full bg-blue-600 text-white px-10 py-5 rounded-2xl font-black text-lg hover:bg-blue-700 transition-all shadow-2xl shadow-blue-900 mb-4"
                      >
                         Submit Agent
                      </button>
                      <p className="text-xs font-bold text-gray-500">Developer SDK Documentation ↗</p>
                   </div>
                </div>
             </div>

             <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
                {filteredStoreAgents.length === 0 ? (
                   <div className="col-span-full text-center py-32 bg-gray-50 dark:bg-white/5 rounded-[40px] border-2 border-dashed border-gray-200 dark:border-white/10">
                      <Bot size={64} className="mx-auto mb-6 text-gray-300 opacity-20" />
                      <h3 className="text-2xl font-black text-gray-900 dark:text-white mb-2">No community agents found.</h3>
                      <p className="text-gray-500 dark:text-gray-400 font-bold">Be the first to monetize your AI models on Yendoukoa.</p>
                   </div>
                ) : filteredStoreAgents.map((agent) => (
                  <ServiceCard
                    key={agent.id}
                    isStoreItem
                    service={{
                      id: agent.id,
                      name: agent.name,
                      description: agent.description,
                      category: agent.category,
                      icon: Bot,
                      price: agent.price_per_use,
                      type: 'agent'
                    }}
                    onLaunch={launchService}
                  />
                ))}
             </div>
          </div>
        )}

        {activeTab === 'design-store' && (
           <div className="space-y-16">
              <div className="bg-gradient-to-br from-indigo-900 via-purple-900 to-indigo-900 rounded-[40px] p-12 text-white shadow-2xl">
                 <div className="flex flex-col md:flex-row justify-between items-center gap-12">
                    <div className="max-w-2xl">
                       <h2 className="text-5xl font-black mb-6 tracking-tight">Design & API Store</h2>
                       <p className="text-xl text-indigo-100 font-medium leading-relaxed opacity-80">
                          Elite UI/UX kits, landing pages, and production-ready API configurations. Own the code, ship the experience.
                       </p>
                       <div className="mt-8 flex flex-wrap gap-4">
                          {['React', 'Next.js', 'Tailwind', 'Python API', 'Figma'].map(tech => (
                             <span key={tech} className="bg-white/10 px-4 py-1.5 rounded-full text-xs font-black tracking-widest uppercase border border-white/10">
                                {tech}
                             </span>
                          ))}
                       </div>
                    </div>
                    <button
                      onClick={() => { if(!user) setShowLoginModal(true); else setShowDesignRegModal(true); }}
                      className="bg-white text-indigo-900 px-10 py-5 rounded-2xl font-black text-lg hover:bg-indigo-50 transition-all shadow-2xl"
                    >
                       Sell Your Design
                    </button>
                 </div>
              </div>

              <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
                 {filteredStoreDesigns.length === 0 ? (
                    <div className="col-span-full text-center py-32 bg-gray-50 dark:bg-white/5 rounded-[40px] border-2 border-dashed border-gray-200 dark:border-white/10">
                       <Layout size={64} className="mx-auto mb-6 text-gray-300 opacity-20" />
                       <h3 className="text-2xl font-black text-gray-900 dark:text-white mb-2">The design vault is empty.</h3>
                       <p className="text-gray-500 dark:text-gray-400 font-bold">Start listing your premium design assets today.</p>
                    </div>
                 ) : filteredStoreDesigns.map((design) => (
                    <ServiceCard
                      key={design.id}
                      isStoreItem
                      service={{
                        id: design.id,
                        name: design.name,
                        description: design.description,
                        category: design.category,
                        icon: Layout,
                        price: design.price,
                        type: 'design'
                      }}
                      onLaunch={launchService}
                    />
                 ))}
              </div>
           </div>
        )}

        {activeTab === 'dashboard' && (
          <div className="space-y-12">
             {!user ? (
                <div className="bg-white dark:bg-[#121212] p-16 rounded-[40px] shadow-xl border border-gray-100 dark:border-white/5 text-center">
                   <div className="w-24 h-24 bg-blue-50 dark:bg-blue-900/20 rounded-full flex items-center justify-center mx-auto mb-8">
                      <UserIcon size={48} className="text-blue-600" />
                   </div>
                   <h2 className="text-3xl font-black text-gray-900 dark:text-white mb-4 tracking-tight">Access Your Workspace</h2>
                   <p className="text-gray-500 dark:text-gray-400 font-medium mb-10 max-w-sm mx-auto">Please login to manage your credits, files, and community contributions.</p>
                   <button onClick={() => setShowLoginModal(true)} className="bg-blue-600 text-white px-10 py-4 rounded-2xl font-black hover:bg-blue-700 shadow-xl shadow-blue-100 transition-all">
                      Login or Register
                   </button>
                </div>
             ) : (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
                   {/* Main Stats */}
                   <div className="lg:col-span-2 space-y-12">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                         <div className="bg-white dark:bg-[#121212] p-10 rounded-[40px] shadow-sm border border-gray-100 dark:border-white/5 relative group overflow-hidden">
                            <div className="absolute top-0 right-0 p-8 text-blue-100 dark:text-blue-900/20 group-hover:text-blue-200 transition-colors">
                               <CreditCard size={120} strokeWidth={1} />
                            </div>
                            <h3 className="text-sm font-black text-blue-600 uppercase tracking-widest mb-2">Total Balance</h3>
                            <p className="text-5xl font-black text-gray-900 dark:text-white tracking-tighter">{credits}</p>
                            <div className="mt-8 flex items-center text-xs font-bold text-gray-400">
                               <CheckCircle2 size={14} className="mr-2 text-green-500" /> Verified by Blockchain
                            </div>
                         </div>
                         <div className="bg-gray-900 p-10 rounded-[40px] shadow-xl text-white relative group">
                            <div className="absolute bottom-0 right-0 p-8 text-white/5">
                               <Zap size={140} strokeWidth={1} />
                            </div>
                            <h3 className="text-sm font-black text-blue-400 uppercase tracking-widest mb-2">Developer Earnings</h3>
                            <p className="text-5xl font-black text-white tracking-tighter">${Math.round(credits * 0.1)}</p>
                            <button className="mt-8 bg-blue-600 text-white px-6 py-2.5 rounded-xl text-xs font-black hover:bg-blue-500 transition-colors">
                               Withdraw Funds
                            </button>
                         </div>
                      </div>

                      {/* File Manager */}
                      <div className="bg-white dark:bg-[#121212] rounded-[40px] shadow-sm border border-gray-100 dark:border-white/5 overflow-hidden">
                         <div className="px-10 py-8 border-b border-gray-50 dark:border-white/5 flex justify-between items-center">
                            <h3 className="text-xl font-black tracking-tight dark:text-white">Knowledge Vault</h3>
                            <label className="cursor-pointer bg-gray-50 dark:bg-white/5 text-gray-900 dark:text-gray-300 px-6 py-2.5 rounded-xl text-sm font-black hover:bg-gray-100 dark:hover:bg-white/10 border border-gray-200 dark:border-white/10 transition-all flex items-center">
                               <Plus size={18} className="mr-2" /> Upload
                               <input type="file" className="hidden" onChange={handleFileUpload} />
                            </label>
                         </div>
                         <div className="p-10">
                            {userFiles.length === 0 ? (
                               <div className="text-center py-20">
                                  <Database size={48} className="mx-auto mb-6 text-gray-200 opacity-20" />
                                  <p className="text-gray-400 font-bold uppercase tracking-widest text-xs">No stored artifacts</p>
                               </div>
                            ) : (
                               <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                  {userFiles.map(file => (
                                     <div key={file.id} className="p-5 border border-gray-100 dark:border-white/5 rounded-2xl bg-gray-50/50 dark:bg-white/5 hover:bg-white dark:hover:bg-white/10 hover:shadow-lg transition-all group flex items-center justify-between">
                                        <div className="flex items-center min-w-0">
                                           <div className="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center text-blue-600 mr-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                                              <FileText size={20} />
                                           </div>
                                           <div className="truncate">
                                              <p className="font-black text-sm text-gray-900 dark:text-white truncate">{file.filename}</p>
                                              <p className="text-[10px] text-gray-400 font-bold uppercase tracking-widest mt-1">{file.file_type}</p>
                                           </div>
                                        </div>
                                        <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                           <button onClick={() => handleDeleteFile(file.id)} className="p-2 text-gray-400 hover:text-red-600"><Trash2 size={16} /></button>
                                        </div>
                                     </div>
                                  ))}
                               </div>
                            )}
                         </div>
                      </div>
                   </div>

                   {/* Sidebar Info */}
                   <div className="space-y-8">
                      <div className="bg-white dark:bg-[#121212] p-8 rounded-[40px] shadow-sm border border-gray-100 dark:border-white/5">
                         <h3 className="font-black text-gray-900 dark:text-white mb-6 uppercase tracking-widest text-xs">Account Status</h3>
                         <div className="space-y-6">
                            <div className="flex items-center justify-between">
                               <span className="text-sm font-bold text-gray-500">Subscription</span>
                               <span className="px-3 py-1 bg-green-50 dark:bg-green-900/20 text-green-600 rounded-lg text-[10px] font-black uppercase tracking-widest border border-green-100 dark:border-green-900/30">Pro Active</span>
                            </div>
                            <div className="flex items-center justify-between">
                               <span className="text-sm font-bold text-gray-500">API Access</span>
                               <span className="text-sm font-black text-gray-900 dark:text-white">Enterprise</span>
                            </div>
                            <div className="flex items-center justify-between">
                               <span className="text-sm font-bold text-gray-500">Identity</span>
                               <span className="text-sm font-black text-gray-900 dark:text-white">Verified</span>
                            </div>
                         </div>
                         <button className="w-full mt-10 bg-gray-900 dark:bg-white dark:text-black text-white py-4 rounded-2xl text-sm font-black hover:bg-black dark:hover:bg-gray-200 transition-all">
                            Manage Billing
                         </button>
                      </div>

                      <div className="bg-blue-600 p-8 rounded-[40px] shadow-xl text-white">
                         <h3 className="font-black mb-4 uppercase tracking-widest text-xs opacity-70">Power Up</h3>
                         <p className="text-xl font-black mb-8 leading-tight">Get 20% extra credits on all top-ups this week.</p>
                         <button className="w-full bg-white text-blue-600 py-4 rounded-2xl text-sm font-black hover:bg-blue-50 transition-all shadow-xl">
                            Buy Credits
                         </button>
                      </div>
                   </div>
                </div>
             )}
          </div>
        )}
      </main>

      {/* Service Execution Modal */}
      <Modal
        isOpen={showServiceModal}
        onClose={() => { stopCamera(); setShowServiceModal(false); }}
        title={`Deploy: ${selectedService?.name}`}
      >
        {!serviceResponse ? (
          <form onSubmit={handleServiceExecution} className="space-y-8">
             {selectedService?.id === 'marketing' && (
                <div className="bg-gray-50 dark:bg-white/5 p-6 rounded-2xl border border-gray-100 dark:border-white/5">
                   <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-4">Service Mode</label>
                   <div className="grid grid-cols-2 gap-4">
                      <button
                        type="button"
                        onClick={() => setExecutionParams({ ...executionParams, type: 'bot' })}
                        className={`p-4 rounded-xl border-2 transition-all flex flex-col items-center space-y-2 ${executionParams.type !== 'video' ? 'bg-blue-600 text-white border-blue-600 shadow-lg' : 'bg-white dark:bg-white/5 text-gray-500 border-gray-100 dark:border-white/5 hover:border-blue-200'}`}
                      >
                         <Bot size={24} />
                         <span className="text-xs font-black">Bot & Strategy</span>
                      </button>
                      <button
                        type="button"
                        onClick={() => setExecutionParams({ ...executionParams, type: 'video' })}
                        className={`p-4 rounded-xl border-2 transition-all flex flex-col items-center space-y-2 ${executionParams.type === 'video' ? 'bg-blue-600 text-white border-blue-600 shadow-lg' : 'bg-white dark:bg-white/5 text-gray-500 border-gray-100 dark:border-white/5 hover:border-blue-200'}`}
                      >
                         <Video size={24} />
                         <span className="text-xs font-black">Video Gen</span>
                      </button>
                   </div>
                </div>
             )}

             {(selectedService?.id === 'visual-intel' || selectedService?.category === 'Advanced') && (
                <div>
                   <label className="block text-xs font-black text-gray-400 uppercase tracking-widest mb-4">Multimodal Input</label>
                   <div className="relative group overflow-hidden rounded-[32px] border-2 border-dashed border-gray-200 dark:border-white/10 bg-gray-50/50 dark:bg-white/5 min-h-[200px] flex items-center justify-center">
                      {isCameraActive ? (
                         <div className="w-full h-full p-4 flex flex-col items-center">
                            <video ref={videoRef} autoPlay playsInline className="w-full max-w-sm rounded-2xl shadow-2xl mb-4 border-4 border-white dark:border-white/10" />
                            <div className="flex space-x-3">
                               {!isRecording ? (
                                  <>
                                     <button type="button" onClick={capturePhoto} className="p-4 bg-blue-600 text-white rounded-2xl shadow-xl hover:scale-105 transition-transform"><Camera size={24} /></button>
                                     <button type="button" onClick={startRecording} className="p-4 bg-red-600 text-white rounded-2xl shadow-xl hover:scale-105 transition-transform"><Play size={24} /></button>
                                  </>
                               ) : (
                                  <button type="button" onClick={stopRecording} className="p-4 bg-gray-900 dark:bg-white dark:text-black text-white rounded-2xl shadow-xl animate-pulse"><X size={24} /></button>
                               )}
                               <button type="button" onClick={stopCamera} className="p-4 bg-white dark:bg-white/10 text-gray-400 rounded-2xl border border-gray-100 dark:border-white/5"><X size={24} /></button>
                            </div>
                         </div>
                      ) : capturedMedia ? (
                        <div className="w-full h-full p-4 flex flex-col items-center">
                           {capturedMedia.type.startsWith('image') ? (
                              <img src={capturedMedia.data} className="w-full max-w-sm rounded-2xl shadow-2xl mb-4 border-4 border-white dark:border-white/10" />
                           ) : (
                              <video src={capturedMedia.data} controls className="w-full max-w-sm rounded-2xl shadow-2xl mb-4 border-4 border-white dark:border-white/10" />
                           )}
                           <button type="button" onClick={() => { setCapturedMedia(null); startCamera(); }} className="text-blue-600 font-black text-xs uppercase tracking-widest hover:underline">Retake Capture</button>
                        </div>
                      ) : (
                        <button type="button" onClick={startCamera} className="flex flex-col items-center space-y-4 text-gray-400 group-hover:text-blue-600 transition-colors">
                           <div className="w-16 h-16 rounded-full bg-white dark:bg-white/10 border border-gray-100 dark:border-white/5 flex items-center justify-center shadow-sm group-hover:scale-110 transition-transform">
                              <Camera size={32} />
                           </div>
                           <span className="text-xs font-black uppercase tracking-widest">Enable Camera Input</span>
                        </button>
                      )}
                   </div>
                </div>
             )}

             <div className="space-y-4">
                <label className="block text-xs font-black text-gray-400 uppercase tracking-widest">System Instructions</label>
                <textarea
                   className="w-full bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-[24px] p-6 text-sm font-medium focus:outline-none focus:ring-4 focus:ring-blue-100 focus:bg-white dark:focus:bg-white/10 transition-all min-h-[160px] dark:text-white"
                   placeholder={`What should the ${selectedService?.name} execute?`}
                   value={servicePrompt}
                   onChange={(e) => setServicePrompt(e.target.value)}
                   required={!executionParams.execute}
                />
             </div>

             <div className="flex items-center justify-between pt-8 border-t border-gray-50 dark:border-white/10">
                <div className="flex flex-col">
                   <span className="text-xs font-black text-gray-400 uppercase tracking-widest">Cost for session</span>
                   <span className="text-xl font-black text-gray-900 dark:text-white">{selectedService?.price || 50} Credits</span>
                </div>
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-blue-600 text-white px-10 py-5 rounded-2xl font-black text-lg hover:bg-blue-700 transition-all shadow-2xl shadow-blue-100 active:scale-95 disabled:opacity-50 flex items-center"
                >
                  {loading && <Loader2 size={20} className="mr-2 animate-spin" />}
                  {loading ? 'Processing Agent...' : 'Launch Session'}
                </button>
             </div>
          </form>
        ) : (
          <div className="space-y-8 animate-fade-in">
             <div className="bg-gray-50 dark:bg-white/5 rounded-[32px] p-8 border border-gray-100 dark:border-white/10 max-h-[500px] overflow-y-auto">
                <p className="text-gray-800 dark:text-gray-200 font-medium leading-relaxed whitespace-pre-wrap selection:bg-blue-100">{serviceResponse}</p>
             </div>
             <div className="flex flex-wrap gap-4 justify-end">
                <button onClick={() => setServiceResponse('')} className="bg-white dark:bg-white/10 border border-gray-200 dark:border-white/5 text-gray-900 dark:text-white px-8 py-4 rounded-2xl font-black text-sm hover:bg-gray-50 dark:hover:bg-white/20 transition-all">Try Again</button>
                <button onClick={handleSaveToStorage} disabled={loading} className="bg-green-600 text-white px-8 py-4 rounded-2xl font-black text-sm hover:bg-green-700 shadow-xl shadow-green-100 flex items-center">
                   <Save size={18} className="mr-2" /> {loading ? 'Saving...' : 'Save to Vault'}
                </button>
                <button onClick={() => setShowServiceModal(false)} className="bg-gray-900 dark:bg-white dark:text-black text-white px-8 py-4 rounded-2xl font-black text-sm hover:bg-black shadow-xl">Done</button>
             </div>
          </div>
        )}
      </Modal>

      {/* Auth Modal */}
      <Modal
        isOpen={showLoginModal}
        onClose={() => setShowLoginModal(false)}
        title={modalMode === 'register' ? 'Join the Future' : 'Welcome Back'}
        maxWidth="max-w-md"
      >
        <form onSubmit={handleAuthSubmit} className="space-y-6">
           <div className="w-20 h-20 bg-blue-50 dark:bg-blue-900/20 rounded-3xl flex items-center justify-center mx-auto mb-10">
              {modalMode === 'register' ? <UserIcon size={32} className="text-blue-600" /> : <Key size={32} className="text-blue-600" />}
           </div>

           {modalMode === 'register' ? (
              <div className="space-y-2">
                 <label className="text-xs font-black text-gray-400 uppercase tracking-widest ml-1">Username</label>
                 <input
                    type="text"
                    className="w-full bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-sm font-bold focus:outline-none focus:ring-4 focus:ring-blue-100 transition-all dark:text-white"
                    placeholder="Choose your handle"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                 />
              </div>
           ) : (
              <div className="space-y-2">
                 <label className="text-xs font-black text-gray-400 uppercase tracking-widest ml-1">API Key</label>
                 <input
                    type="password"
                    className="w-full bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-sm font-bold focus:outline-none focus:ring-4 focus:ring-blue-100 transition-all dark:text-white"
                    placeholder="Paste your access key"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    required
                 />
              </div>
           )}

           <button
             type="submit"
             disabled={loading}
             className="w-full bg-blue-600 text-white py-5 rounded-2xl font-black text-lg hover:bg-blue-700 shadow-2xl shadow-blue-100 transition-all flex items-center justify-center"
           >
              {loading && <Loader2 size={24} className="mr-2 animate-spin" />}
              {loading ? 'Authenticating...' : modalMode === 'register' ? 'Create Account' : 'Sign In'}
           </button>

           <div className="text-center">
              <button
                type="button"
                onClick={() => setModalMode(modalMode === 'register' ? 'login' : 'register')}
                className="text-sm font-black text-blue-600 hover:underline"
              >
                {modalMode === 'register' ? 'Already have a key?' : 'New to Yendoukoa?'}
              </button>
           </div>
        </form>
      </Modal>

      {/* Admin/Reg Modals */}
      {showAgentRegModal && (
        <Modal isOpen={showAgentRegModal} onClose={() => setShowAgentRegModal(false)} title="Register AI Agent">
           <form onSubmit={handleAgentRegistration} className="space-y-6">
              <input className="w-full bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-sm font-bold dark:text-white" placeholder="Agent Name" value={newAgent.name} onChange={e => setNewAgent({...newAgent, name: e.target.value})} required />
              <textarea className="w-full bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-sm font-bold min-h-[120px] dark:text-white" placeholder="Detailed Description" value={newAgent.description} onChange={e => setNewAgent({...newAgent, description: e.target.value})} required />
              <input className="w-full bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-sm font-bold dark:text-white" placeholder="Endpoint URL" value={newAgent.endpoint_url} onChange={e => setNewAgent({...newAgent, endpoint_url: e.target.value})} required />
              <div className="grid grid-cols-2 gap-4">
                 <input type="number" className="bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-sm font-bold dark:text-white" placeholder="Price (Credits)" value={newAgent.price_per_use} onChange={e => setNewAgent({...newAgent, price_per_use: parseInt(e.target.value)})} required />
                 <select className="bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-sm font-bold dark:text-white" value={newAgent.category} onChange={e => setNewAgent({...newAgent, category: e.target.value})}>
                    <option>General</option><option>Development</option><option>Business</option><option>Security</option>
                 </select>
              </div>
              <button type="submit" disabled={loading} className="w-full bg-blue-600 text-white py-5 rounded-2xl font-black flex items-center justify-center">
                 {loading && <Loader2 size={24} className="mr-2 animate-spin" />}
                 Register Agent
              </button>
           </form>
        </Modal>
      )}

      {showDesignRegModal && (
        <Modal isOpen={showDesignRegModal} onClose={() => setShowDesignRegModal(false)} title="List Design Asset">
           <form onSubmit={handleDesignRegistration} className="space-y-6">
              <input className="w-full bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-sm font-bold dark:text-white" placeholder="Asset Name" value={newDesign.name} onChange={e => setNewDesign({...newDesign, name: e.target.value})} required />
              <textarea className="w-full bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-sm font-bold min-h-[120px] dark:text-white" placeholder="Description" value={newDesign.description} onChange={e => setNewDesign({...newDesign, description: e.target.value})} required />
              <textarea className="w-full bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-xs font-mono min-h-[120px] dark:text-white" placeholder="Content (Code/JSON)" value={newDesign.content} onChange={e => setNewDesign({...newDesign, content: e.target.value})} required />
              <div className="grid grid-cols-2 gap-4">
                 <input type="number" className="bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-sm font-bold dark:text-white" placeholder="Price (Credits)" value={newDesign.price} onChange={e => setNewDesign({...newDesign, price: parseInt(e.target.value)})} required />
                 <select className="bg-gray-50 dark:bg-white/5 border border-gray-100 dark:border-white/10 rounded-2xl p-5 text-sm font-bold dark:text-white" value={newDesign.category} onChange={e => setNewDesign({...newDesign, category: e.target.value})}>
                    <option>Web</option><option>Mobile</option><option>API</option><option>Landing Page</option>
                 </select>
              </div>
              <button type="submit" disabled={loading} className="w-full bg-purple-600 text-white py-5 rounded-2xl font-black flex items-center justify-center">
                 {loading && <Loader2 size={24} className="mr-2 animate-spin" />}
                 List Asset
              </button>
           </form>
        </Modal>
      )}

      <Footer />
    </div>
  );
};

export default App;
