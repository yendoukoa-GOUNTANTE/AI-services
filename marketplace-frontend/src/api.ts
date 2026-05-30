import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const setAuthToken = (token: string | null) => {
  if (token) {
    apiClient.defaults.headers.common['X-API-Key'] = token;
  } else {
    delete apiClient.defaults.headers.common['X-API-Key'];
  }
};

export interface User {
  id: number;
  username: string;
  subscription_status?: string;
  subscription_plan?: string;
  credits?: number;
}

export interface StoreAgent {
  id: number;
  developer_id: number;
  developer_name: string;
  name: string;
  description: string;
  price_per_use: number;
  category: string;
  created_at: string;
}

export interface StoreDesign {
  id: number;
  developer_id: number;
  developer_name: string;
  name: string;
  description: string;
  preview_url?: string;
  price: number;
  category: string;
  created_at: string;
}

export interface File {
  id: number;
  filename: string;
  file_type: string;
  content?: string;
  created_at: string;
}

export interface Project {
  id: number;
  title: string;
  description: string;
  image_url: string;
}

export const aiService = {
  generateWebsite: (prompt: string) => apiClient.post('/develop/website', { prompt }),
  debugCode: (prompt: string) => apiClient.post('/debug', { prompt }),
  analyzeWebsite: (url: string) => apiClient.post('/analyze/website', { url }),
  generateSocialPost: (prompt: string) => apiClient.post('/market/post', { prompt }),
  getWeather: (location: string) => apiClient.post('/weather', { location }),
  getFinancialAdvice: (prompt: string) => apiClient.post('/finance/advice', { prompt }),
  getGoogleSitesAssistance: (prompt: string) => apiClient.post('/google-sites/assistance', { prompt }),
  getDiagnosticAssistance: (prompt: string) => apiClient.post('/diagnostic/assistance', { prompt }),
  getMarketingAssistance: (prompt: string) => apiClient.post('/marketing/assistance', { prompt }),
  generateMarketingVideo: (prompt: string) => apiClient.post('/marketing/video', { prompt }),
  getDigitalRepairAssistance: (prompt: string) => apiClient.post('/digital-repair/assistance', { prompt }),
  getInvestmentTradingAssistance: (prompt: string) => apiClient.post('/investment-trading/assistance', { prompt }),
  getAutoGPTAssistance: (prompt: string) => apiClient.post('/autogpt/assistance', { prompt }),
  getIaaSAssistance: (prompt: string) => apiClient.post('/iaas/assistance', { prompt }),
  getPaaSAssistance: (prompt: string) => apiClient.post('/paas/assistance', { prompt }),
  getSaaSAssistance: (prompt: string) => apiClient.post('/saas/assistance', { prompt }),
  getITaaSAssistance: (prompt: string) => apiClient.post('/itaas/assistance', { prompt }),
  getGumloopAssistance: (prompt: string, execute = false, pipelineId?: string, inputs?: any) =>
    apiClient.post('/gumloop/assistance', { prompt, execute, pipeline_id: pipelineId, inputs }),
  getN8nAssistance: (prompt: string, execute = false, webhookUrl?: string, payload?: any) =>
    apiClient.post('/n8n/assistance', { prompt, execute, webhook_url: webhookUrl, payload }),
  getLamaticAssistance: (prompt: string, execute = false, workflowId?: string) =>
    apiClient.post('/lamatic/assistance', { prompt, execute, workflow_id: workflowId }),
  getMalwareDefenseAssistance: (prompt: string) => apiClient.post('/malware-defense/assistance', { prompt }),
  getUSSDBlockchainAssistance: (prompt: string) => apiClient.post('/ussd-blockchain/assistance', { prompt }),
  getBlockchainSponsoring: (prompt: string) => apiClient.post('/blockchain/sponsoring', { prompt }),
  getFineTuningAssistance: (prompt: string) => apiClient.post('/fine-tuner/assistance', { prompt }),
  getRAGTuningAssistance: (prompt: string) => apiClient.post('/rag-tuning/assistance', { prompt }),
  getRouterCapacityAssistance: (prompt: string) => apiClient.post('/router/assistance', { prompt }),
  getOpenCollectiveAssistance: (prompt: string) => apiClient.post('/sponsorship/open-collective', { prompt }),
  getPatreonAssistance: (prompt: string) => apiClient.post('/sponsorship/patreon', { prompt }),
  getVideoProductionAssistance: (prompt: string) => apiClient.post('/video/assistance', { prompt }),
  getPodcastAssistance: (prompt: string) => apiClient.post('/podcast/assistance', { prompt }),
  getZapierAssistance: (prompt: string) => apiClient.post('/zapier/assistance', { prompt }),
  getOdooAssistance: (prompt: string) => apiClient.post('/odoo/assistance', { prompt }),
  getSageAssistance: (prompt: string) => apiClient.post('/sage/assistance', { prompt }),
  getGovernmentAssistance: (prompt: string) => apiClient.post('/government/assistance', { prompt }),
  getTogoAssistance: (prompt: string) => apiClient.post('/togo/assistance', { prompt }),
  getXeroAssistance: (prompt: string) => apiClient.post('/xero/assistance', { prompt }),
  getPublicPolicyAssistance: (prompt: string) => apiClient.post('/government/policy', { prompt }),
  getCitizenEngagementAssistance: (prompt: string) => apiClient.post('/government/engagement', { prompt }),
  getSmartCityAssistance: (prompt: string) => apiClient.post('/government/smart-city', { prompt }),
  getBiasDetectionAssistance: (prompt: string) => apiClient.post('/government/bias-detection', { prompt }),
  getMilitaryAssistance: (prompt: string) => apiClient.post('/military/assistance', { prompt }),
  getGendarmerieAssistance: (prompt: string) => apiClient.post('/gendarmerie/assistance', { prompt }),
  getPoliceAssistance: (prompt: string) => apiClient.post('/police/assistance', { prompt }),
  getSecurityOptimization: (prompt: string) => apiClient.post('/security/optimization', { prompt }),
  getCybersecuritySentinel: (prompt: string) => apiClient.post('/security/sentinel', { prompt }),
  getConflictDebugAssistance: (prompt: string, mediaData?: string, mimeType?: string) => apiClient.post('/conflict-debug/assistance', { prompt, media_data: mediaData, mime_type: mimeType }),
  executeLangflow: (prompt: string) => apiClient.post('/langflow/execute', { prompt }),
  getAutoMLFeatureEngineering: (prompt: string) => apiClient.post('/automl/feature-engineering', { prompt }),
  getAutoMLHyperparameterTuning: (prompt: string) => apiClient.post('/automl/hyperparameter-tuning', { prompt }),
  getAutoMLModelSelection: (prompt: string) => apiClient.post('/automl/model-selection', { prompt }),
  getAutoMLMLOps: (prompt: string) => apiClient.post('/automl/mlops', { prompt }),
  getCloudInfrastructureAssistance: (prompt: string) => apiClient.post('/cloud-infrastructure/assistance', { prompt }),
  getDomainCodexAssistance: (prompt: string) => apiClient.post('/domain-codex/assistance', { prompt }),
  getMonetizationAdvice: (prompt: string) => apiClient.post('/business/monetization', { prompt }),
  getPartnershipAdvice: (prompt: string) => apiClient.post('/business/partnership', { prompt }),
  getFundraisingAdvice: (prompt: string) => apiClient.post('/business/fundraising', { prompt }),
  getLlamaIntelligence: (prompt: string) => apiClient.post('/llama/intelligence', { prompt }),
  getLlamaGuard: (prompt: string) => apiClient.post('/llama/guard', { prompt }),
  getNemotronReasoning: (prompt: string) => apiClient.post('/nvidia/nemotron', { prompt }),
  getMixtralMultilingual: (prompt: string) => apiClient.post('/nvidia/mixtral', { prompt }),
  getClaudeIntelligence: (prompt: string) => apiClient.post('/anthropic/intelligence', { prompt }),
  getClaudeCoding: (prompt: string) => apiClient.post('/anthropic/coding', { prompt }),
  getGitHubModelsAssistance: (prompt: string, modelName = 'gpt-4o') => apiClient.post('/github-models/assistance', { prompt, model_name: modelName }),
  getGitHubCopilotChat: (prompt: string) => apiClient.post('/copilot-chat/assistance', { prompt }),
  getLanguageSpecialist: (prompt: string) => apiClient.post('/language/specialist', { prompt }),
  getLogoThumbnailAssistance: (prompt: string) => apiClient.post('/logo-thumbnail/assistance', { prompt }),
  getVisualAnalysis: (prompt: string, mediaData?: string, mimeType?: string) => apiClient.post('/visual/analysis', { prompt, media_data: mediaData, mime_type: mimeType }),
  genericAssistance: (systemMessage: string, prompt: string, mediaData?: string, mimeType?: string) => apiClient.post('/generic/assistance', { system_message: systemMessage, prompt, media_data: mediaData, mime_type: mimeType }),
  getDeepMindImage: (prompt: string) => apiClient.post('/deepmind/image', { prompt }),
  getDeepMindVideo: (prompt: string) => apiClient.post('/deepmind/video', { prompt }),
  getAntigravityAgentAssistance: (prompt: string) => apiClient.post('/v1/antigravity/agent', { prompt }),
  getGeminiSparkAssistance: (prompt: string) => apiClient.post('/v1/gemini/spark', { prompt }),
  getGitHubCopilotCoding: (prompt: string) => apiClient.post('/v1/copilot/coding', { prompt }),
};

export const userService = {
  register: (username: string) => apiClient.post('/register_public', { username }),
  login: (api_key: string) => apiClient.post('/login', { api_key }),
  getMe: () => apiClient.get<User>('/me_api'),
  getProjects: () => apiClient.get<Project[]>('/portfolio/projects'),
  createProject: (title: string, description: string) => apiClient.post<Project>('/projects', { title, description }),
};

export const storeService = {
  getAgents: (category?: string) => apiClient.get<StoreAgent[]>('/store/agents', { params: { category } }),
  registerAgent: (agent: Partial<StoreAgent> & { endpoint_url: string }) => apiClient.post('/store/agents', agent),
  getDesigns: (category?: string) => apiClient.get<StoreDesign[]>('/store/designs', { params: { category } }),
  registerDesign: (design: Partial<StoreDesign> & { content?: string }) => apiClient.post('/store/designs', design),
  executeAgent: (agentId: number, prompt: string) => apiClient.post('/store/execute', { agent_id: agentId, prompt }),
  purchaseDesign: (designId: number) => apiClient.post('/store/purchase', { design_id: designId }),
};

export const fileService = {
  getFiles: () => apiClient.get<File[]>('/files'),
  uploadFile: (file: File | any) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  createDoc: (filename: string, content: string, file_type = 'document') =>
    apiClient.post('/files/create-doc', { filename, content, file_type }),
  getFile: (fileId: number) => apiClient.get<File>(`/files/${fileId}`),
  deleteFile: (fileId: number) => apiClient.delete(`/files/${fileId}`),
};

export const paymentService = {
  getConfig: () => apiClient.get('/v1/config'),
  createPaymentIntent: (amount: number, currency: string) => apiClient.post('/payment/create-payment-intent', { amount, currency }),
  createSubscriptionCheckout: (plan: string) => apiClient.post('/payment/create-subscription-checkout', { plan }),
};

export default apiClient;
