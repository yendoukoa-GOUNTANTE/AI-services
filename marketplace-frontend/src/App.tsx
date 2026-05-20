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
  Video
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { userService, aiService, paymentService, setAuthToken, type User } from './api';
import axios from 'axios';

interface AIService {
  id: string;
  name: string;
  category: string;
  icon: LucideIcon;
  description: string;
}

const AI_SERVICES: AIService[] = [
  { id: 'langflow', name: 'Langflow Executor', category: 'Advanced', icon: Zap, description: 'Execute complex AI workflows using Langflow.' },
  { id: 'website', name: 'Website Developer', category: 'Development', icon: Globe, description: 'Generate multi-section HTML/CSS websites.' },
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
  { id: 'togo-gov', name: 'Togo Public Service', category: 'Public', icon: Building2, description: 'Elite AI for Togolese public services, government administration, and national security.' },
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
  { id: 'marketing', name: 'Marketing & Bot Specialist', category: 'Business', icon: Mail, description: 'Expert e-mail, SMS, and bot marketing & management.' },
  { id: 'investment', name: 'Investment Specialist', category: 'Business', icon: TrendingUp, description: 'Investment optimization and trading assistance.' },
  { id: 'autogpt', name: 'AutoGPT Agent', category: 'Advanced', icon: Bot, description: 'Autonomous agent for multi-step task planning and strategy.' },
  { id: 'cloud-infra', name: 'Cloud Infra Architect', category: 'Infrastructure', icon: Server, description: 'Expert in secure IPs, DNS, and cloud server creation.' },
  { id: 'domain-codex', name: 'Domain Codex Designer', category: 'Infrastructure', icon: Layout, description: 'Elite custom domain design and USSP infrastructure architect.' },
  { id: 'iaas', name: 'IaaS Specialist', category: 'Infrastructure', icon: Cpu, description: 'Infrastructure as a Service expert for virtualized resources.' },
  { id: 'paas', name: 'PaaS Specialist', category: 'Infrastructure', icon: Cloud, description: 'Platform as a Service expert for application development environments.' },
  { id: 'saas', name: 'SaaS Specialist', category: 'Infrastructure', icon: Globe, description: 'Software as a Service expert for internet-delivered applications.' },
  { id: 'itaas', name: 'ITaaS Specialist', category: 'Infrastructure', icon: Layout, description: 'IT as a Service expert for comprehensive IT service delivery.' },
  { id: 'conflict-debug', name: 'Multi-Model Debugger', category: 'Development', icon: ShieldCheck, description: 'Debug and resolve conflicts using Gemini, ChatGPT, Claude, and NVIDIA.' },
  { id: 'automl-feat', name: 'AutoML Feature Eng', category: 'Development', icon: Binary, description: 'Automated feature engineering and data preparation.' },
  { id: 'automl-tune', name: 'AutoML Tuner', category: 'Development', icon: TrendingUp, description: 'Automated hyperparameter optimization and tuning.' },
  { id: 'automl-select', name: 'AutoML Selector', category: 'Development', icon: Microscope, description: 'Automated model selection and evaluation.' },
  { id: 'automl-mlops', name: 'AutoML MLOps', category: 'Development', icon: Zap, description: 'Automated ML pipelines and MLOps strategy.' },
  { id: 'monetization', name: 'Monetization Expert', category: 'Business', icon: DollarSign, description: 'Strategic advice on revenue generation and subscriptions.' },
  { id: 'partnership', name: 'Partnership Specialist', category: 'Business', icon: Handshake, description: 'Identify and nurture strategic business alliances.' },
  { id: 'fundraising', name: 'Fundraising Strategist', category: 'Business', icon: PiggyBank, description: 'Comprehensive plans for securing project funding.' },
  { id: 'llama-intel', name: 'Llama Intelligence', category: 'Advanced', icon: Brain, description: 'Deep reasoning and data-driven insights powered by Llama 3.1.' },
  { id: 'llama-guard', name: 'Llama Guard', category: 'Security', icon: ShieldCheck, description: 'AI safety and content moderation using Llama Guard.' },
  { id: 'nemotron', name: 'Nemotron Reasoner', category: 'Advanced', icon: Zap, description: 'Elite reasoning and complex problem solving powered by NVIDIA Nemotron.' },
  { id: 'mixtral', name: 'Mixtral Multilingual', category: 'Advanced', icon: Globe, description: 'High-quality multilingual assistance powered by Mixtral 8x7B.' },
  { id: 'claude-intel', name: 'Claude Intelligence', category: 'Advanced', icon: Brain, description: 'Deep reasoning and strategic analysis powered by Anthropic Claude.' },
  { id: 'claude-coder', name: 'Claude Coder', category: 'Development', icon: Code2, description: 'Elite code generation and architectural advice powered by Anthropic Claude.' },
  { id: 'malware-defense', name: 'Malware Defender', category: 'Security', icon: ShieldX, description: 'Elite specialist for detecting, preventing, and removing all types of malware.' },
  { id: 'ussd-blockchain', name: 'USSD Blockchain Expert', category: 'Development', icon: Smartphone, description: 'Design and create USSD applications integrated with blockchain technology.' },
  { id: 'visual-intel', name: 'Visual Intelligence', category: 'Advanced', icon: Camera, description: 'Analyze images and videos captured from your camera to provide insights and descriptions.' }
];

const App: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('marketplace');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [user, setUser] = useState<User | null>(null);
  const [credits, setCredits] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [modalMode, setModalMode] = useState<'login' | 'register'>('register');
  const [username, setUsername] = useState('');
  const [apiKey, setApiKey] = useState('');
  const [selectedService, setSelectedService] = useState<AIService | null>(null);
  const [showServiceModal, setShowServiceModal] = useState(false);
  const [servicePrompt, setServicePrompt] = useState('');
  const [serviceResponse, setServiceResponse] = useState('');
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [capturedMedia, setCapturedMedia] = useState<{data: string, type: string} | null>(null);
  const videoRef = React.useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = React.useRef<MediaRecorder | null>(null);
  const chunksRef = React.useRef<Blob[]>([]);

  useEffect(() => {
    const savedApiKey = localStorage.getItem('globalApiKey');
    if (savedApiKey) {
      setAuthToken(savedApiKey);
      fetchUserData();
    }

    // Check for payment callback
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('payment') === 'success') {
      setActiveTab('dashboard');
      alert('Payment successful! Your subscription has been updated.');
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (urlParams.get('payment') === 'cancel') {
      setActiveTab('dashboard');
      alert('Payment cancelled.');
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const response = await userService.getMe();
      setUser(response.data);
      setCredits(1000);
      setError(null);
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

      switch (selectedService.id) {
        case 'visual-intel':
          response = await aiService.getVisualAnalysis(servicePrompt, mediaData, mimeType);
          break;
        case 'website':
          response = await aiService.generateWebsite(servicePrompt);
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
          response = await aiService.getMarketingAssistance(servicePrompt);
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
        case 'malware-defense':
          response = await aiService.getMalwareDefenseAssistance(servicePrompt);
          break;
        case 'ussd-blockchain':
          response = await aiService.getUSSDBlockchainAssistance(servicePrompt);
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
        case 'conflict-debug':
          response = await aiService.getConflictDebugAssistance(servicePrompt, mediaData, mimeType);
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
        case 'game':
          response = await aiService.getGameDeveloper(servicePrompt);
          break;
        case 'backend':
          response = await aiService.getBackendArchitect(servicePrompt);
          break;
        case 'blockchain':
          response = await aiService.getBlockchainExpert(servicePrompt);
          break;
        case 'eshop':
          response = await aiService.getEshopAssistance(servicePrompt);
          break;
        case 'investigation':
          response = await aiService.getCyberInvestigation(servicePrompt);
          break;
        case 'biotech':
          response = await aiService.getBiotechAssistance(servicePrompt);
          break;
        case 'logistics':
          response = await aiService.getLogisticsAssistance(servicePrompt);
          break;
        case 'it-ops':
          response = await aiService.getITOpsAssistance(servicePrompt);
          break;
        case 'education':
          response = await aiService.getScienceEducation(servicePrompt);
          break;
        case 'verification':
          response = await aiService.getFakeContentVerification(servicePrompt);
          break;
        case 'maintenance':
          response = await aiService.getHardwareMaintenance(servicePrompt);
          break;
        case 'researcher':
          response = await aiService.getAIResearcher(servicePrompt);
          break;
        case 'legal':
          response = await aiService.getLegalAssistance(servicePrompt);
          break;
        default:
          // Fallback for newer services
          response = await aiService.genericAssistance(
            `You are the ${selectedService.name}. ${selectedService.description}`,
            servicePrompt,
            mediaData,
            mimeType
          );
      }
      setServiceResponse(response.data.message || response.data.promotion_text || "Service executed successfully.");
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

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      {/* Navigation */}
      <nav className="bg-white border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-2xl font-bold text-blue-600">Yendoukoa AI</span>
              <div className="hidden md:ml-6 md:flex md:space-x-8">
                <button
                  onClick={() => setActiveTab('marketplace')}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'marketplace' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}
                >
                  Marketplace
                </button>
                <button
                  onClick={() => setActiveTab('dashboard')}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'dashboard' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}
                >
                  Dashboard
                </button>
                <button
                  onClick={() => setActiveTab('webbook')}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${activeTab === 'webbook' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'}`}
                >
                  Webbook
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
        {/* Mobile menu */}
        {isMenuOpen && (
          <div className="md:hidden border-t px-4 pt-2 pb-3 space-y-1 bg-white">
            <button
              onClick={() => { setActiveTab('marketplace'); setIsMenuOpen(false); }}
              className={`block w-full text-left px-3 py-2 rounded-md text-base font-medium ${activeTab === 'marketplace' ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50'}`}
            >
              Marketplace
            </button>
            <button
              onClick={() => { setActiveTab('dashboard'); setIsMenuOpen(false); }}
              className={`block w-full text-left px-3 py-2 rounded-md text-base font-medium ${activeTab === 'dashboard' ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50'}`}
            >
              Dashboard
            </button>
            <button
              onClick={() => { setActiveTab('webbook'); setIsMenuOpen(false); }}
              className={`block w-full text-left px-3 py-2 rounded-md text-base font-medium ${activeTab === 'webbook' ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:bg-gray-50'}`}
            >
              Webbook
            </button>
          </div>
        )}
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
                          <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700">Prompt / Requirements</label>
                            <textarea
                              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                              placeholder={`Describe what you need the ${selectedService.name} to do...`}
                              value={servicePrompt}
                              onChange={(e) => setServicePrompt(e.target.value)}
                              rows={5}
                              required
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
      <div className="bg-blue-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl text-center">
            AI Service Marketplace
          </h1>
          <p className="mt-6 text-xl text-blue-100 max-w-3xl mx-auto text-center">
            Discover and utilize professional AI services for your business, development, and personal projects.
          </p>
          <div className="mt-10 max-w-xl mx-auto">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                className="block w-full pl-10 pr-3 py-4 border border-transparent rounded-lg leading-5 bg-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-white focus:border-white sm:text-sm"
                placeholder="Search for AI services..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {activeTab === 'webbook' ? (
          <div className="bg-white p-8 rounded-xl shadow-sm border prose max-w-none">
            <h1 className="text-3xl font-bold mb-6 text-blue-600">Yendoukoa AI: Official Project Webbook</h1>

            <section className="mb-8">
              <h2 className="text-2xl font-bold mb-4">1. Introduction</h2>
              <p>Welcome to the Yendoukoa AI Production Environment. This platform represents the pinnacle of integrated AI services, designed for professional use across various sectors including development, business, security, and public administration.</p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold mb-4">2. Our Ecosystem</h2>
              <p>Yendoukoa AI operates as a unified ecosystem connecting industry-leading AI models (Google Gemini, OpenAI GPT-4o, Anthropic Claude, and NVIDIA Llama) through a single, secure gateway. Our architecture ensures that you always have the most capable model for your specific task.</p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold mb-4">3. Getting Started</h2>
              <ol className="list-decimal pl-5 space-y-2">
                <li><strong>Register:</strong> Create an account to receive your unique API Key.</li>
                <li><strong>API Key:</strong> Keep your API Key secure. It is required for all service executions.</li>
                <li><strong>Credits:</strong> Each service execution consumes credits. You can manage your balance in the Dashboard.</li>
                <li><strong>Subscriptions:</strong> Upgrade to Premium or Pro plans to unlock high-capacity services and monthly credit top-ups.</li>
              </ol>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold mb-4">4. Key Services</h2>
              <ul className="list-disc pl-5 space-y-2">
                <li><strong>Advanced Multi-Model Debugger:</strong> Resolves complex conflicts by synthesizing insights from four major AI providers.</li>
                <li><strong>USSD Blockchain:</strong> Bridges the gap between feature phone technology and modern decentralized finance.</li>
                <li><strong>Public Sector AI:</strong> Specialized tools for Togolese public services and national security.</li>
                <li><strong>Infrastructure as a Service (XaaS):</strong> Elite guidance for IaaS, PaaS, SaaS, and ITaaS deployments.</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold mb-4">5. Security & Privacy</h2>
              <p>We prioritize the security of your data and the integrity of AI-generated content. With integrated Llama Guard and Malware Defender agents, Yendoukoa AI ensures a safe and compliant production environment.</p>
            </section>

            <div className="mt-12 p-6 bg-blue-50 rounded-lg border border-blue-100">
              <p className="text-blue-800 font-bold">Need help? Contact our elite support team at support@yendoukoa.ai</p>
            </div>
          </div>
        ) : activeTab === 'marketplace' ? (
          <div>
            <div className="flex justify-between items-center mb-8">
              <h2 className="text-2xl font-bold text-gray-900">Featured Services</h2>
              <div className="flex space-x-2 overflow-x-auto pb-2">
                {['All', 'Development', 'Business', 'Public', 'Support', 'Security', 'Advanced', 'Infrastructure', 'Science'].map(cat => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`whitespace-nowrap px-4 py-2 rounded-full border text-sm font-medium transition-colors ${
                      selectedCategory === cat
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    {cat}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 gap-y-10 gap-x-6 sm:grid-cols-2 lg:grid-cols-3 xl:gap-x-8">
              {filteredServices.map((service) => (
                <div key={service.id} className="group relative bg-white border rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div className="p-3 bg-blue-50 rounded-lg text-blue-600">
                        <service.icon size={24} />
                      </div>
                      <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">
                        {service.category}
                      </span>
                    </div>
                    <h3 className="text-lg font-bold text-gray-900">
                      <a href={`#${service.id}`}>
                        <span aria-hidden="true" className="absolute inset-0" />
                        {service.name}
                      </a>
                    </h3>
                    <p className="mt-2 text-sm text-gray-500 line-clamp-2">
                      {service.description}
                    </p>
                    <div className="mt-6 flex items-center justify-between">
                      <span className="text-blue-600 font-bold">50 Credits</span>
                      <button
                        onClick={() => {
                          setSelectedService(service);
                          setShowServiceModal(true);
                          setServicePrompt('');
                          setServiceResponse('');
                        }}
                        className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 z-10"
                      >
                        Use Now
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
                    <p className="text-xs text-blue-400 mt-2 italic">* Balance is currently estimated</p>
                    </div>
                    <div className="bg-green-50 p-6 rounded-lg border border-green-100">
                      <p className="text-green-600 text-sm font-medium uppercase">Active Projects</p>
                      <p className="text-3xl font-bold mt-1 text-green-900">3</p>
                    </div>
                    <div className="bg-purple-50 p-6 rounded-lg border border-purple-100">
                      <p className="text-purple-600 text-sm font-medium uppercase">Completed Tasks</p>
                      <p className="text-3xl font-bold mt-1 text-purple-900">12</p>
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
              <span className="text-2xl font-bold text-blue-600">Yendoukoa AI</span>
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
