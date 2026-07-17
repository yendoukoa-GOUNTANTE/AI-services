document.addEventListener('DOMContentLoaded', () => {
    fetchProjects();

    // Global API Key storage for the session
    let globalApiKey = null;

    function getApiKey(message) {
        if (globalApiKey) return globalApiKey;
        const apiKey = prompt(message || "Please enter your API key:");
        if (apiKey) {
            globalApiKey = apiKey;
        }
        return apiKey;
    }

    // --- Meta Pay and Stripe Integration ---

    let stripe;
    let metaAppId;
    const paymentStatus = document.getElementById('payment-status');

    async function fetchConfig() {
        try {
            const response = await fetch('/api/config');
            if (!response.ok) {
                throw new Error('Failed to fetch config');
            }
            const config = await response.json();
            if (!config.stripePublicKey || !config.metaAppId) {
                throw new Error('Stripe or Meta App ID missing from config.');
            }
            stripe = Stripe(config.stripePublicKey);
            metaAppId = config.metaAppId;
            return true;
        } catch (error) {
            console.error('Error fetching config:', error);
            if (paymentStatus) {
                paymentStatus.textContent = `Error: Could not load payment configuration. ${error.message}`;
            }
            return false;
        }
    }

    async function fetchPaymentIntent() {
        try {
            const apiKey = getApiKey("Please enter your API key to make a purchase:");
            if (!apiKey) {
                if(paymentStatus) paymentStatus.textContent = 'API key is required to make a purchase.';
                return null;
            }

            const response = await fetch('/api/v1/payment/create-payment-intent', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': apiKey
                },
                body: JSON.stringify({
                    amount: '10.00',
                    currency: 'usd'
                })
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to create payment intent.');
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching payment intent:', error);
            if (paymentStatus) {
                paymentStatus.textContent = `Error: ${error.message}`;
            }
            return null;
        }
    }

    async function initializeMetaPay() {
        const configLoaded = await fetchConfig();
        if (!configLoaded) return;

        try {
            const paymentClient = new MetaPay.PaymentClient(metaAppId, "V1");
            const canPay = await paymentClient.canPay();

            if (canPay.canPay) {
                renderMetaPayButton(paymentClient);
            } else {
                if (paymentStatus) {
                    paymentStatus.textContent = 'Meta Pay is not available on this device/browser.';
                }
            }
        } catch (err) {
            console.error('Meta Pay SDK Error:', err);
            if (paymentStatus) {
                paymentStatus.textContent = 'Could not initialize Meta Pay. Check your App ID.';
            }
        }
    }

    function renderMetaPayButton(paymentClient) {
        const paymentRequest = {
            "countryCode": "US",
            "currencyCode": "USD",
            "paymentDetails": {
                "displayItems": [{
                    "label": "1000 AI Credits",
                    "amount": { "currency": "USD", "value": "10.00" }
                }],
                "total": {
                    "label": "Total",
                    "amount": { "currency": "USD", "value": "10.00" }
                }
            },
            "paymentOptions": {
                "allowDebit": true,
                "allowPrepaid": true,
                "shippingAddressRequired": false,
                "payerEmailRequired": true,
                "payerNameRequired": true,
                "payerPhoneRequired": false
            }
        };

        const button = paymentClient.fbpayBtn(paymentRequest, {
            "button-type": "buy",
            "button-theme": "dark",
            "width": 200,
            "height": 40
        });

        button.onClick(async () => {
            const paymentIntentData = await fetchPaymentIntent();
            if (!paymentIntentData || !paymentIntentData.clientSecret) {
                return;
            }
            const clientSecret = paymentIntentData.clientSecret;

            try {
                const response = await paymentClient.show(paymentRequest);
                if (response.paymentContainer) {
                    if (paymentStatus) {
                        paymentStatus.textContent = 'Processing payment...';
                    }
                    await handleMetaPayContainer(response.paymentContainer, clientSecret);
                } else {
                    if (paymentStatus) {
                        paymentStatus.textContent = 'Payment cancelled or failed.';
                    }
                }
            } catch (err) {
                console.error('Meta Pay Error:', err);
                if (paymentStatus) {
                    paymentStatus.textContent = `Error: ${err.message}`;
                }
            }
        });

        const container = document.getElementById('meta-pay-button-container');
        if (container) {
            container.innerHTML = '';
            container.appendChild(button);
        }
    }

    async function handleMetaPayContainer(paymentContainer, clientSecret) {
        console.log("Received Meta Pay Container:", paymentContainer);
        console.log("Using Payment Intent Client Secret:", clientSecret);

        if (paymentStatus) {
            paymentStatus.textContent = 'Received payment details from Meta. Final integration with Stripe is pending.';
        }

        // ================== CRITICAL: PENDING IMPLEMENTATION ==================
        // The following step requires knowledge of Stripe's specific integration
        // method for Meta Pay, which is not publicly documented. The code
        // below is a speculative example of how it might work. The actual
        // implementation will depend on the contract between Meta and Stripe.
        //
        // A developer with access to the private documentation will need to
        // replace this placeholder.
        // ======================================================================

        alert("Payment details received from Meta Pay. The final step of charging with Stripe is not yet implemented.");
    }

    if (document.getElementById('meta-pay-button-container')) {
        initializeMetaPay();
    }

    async function fetchProjects() {
        try {
            const response = await fetch('/api/v1/portfolio/projects');
            if (!response.ok) {
                throw new Error('Failed to fetch projects');
            }
            const projects = await response.json();
            renderProjects(projects);
        } catch (error) {
            console.error('Error fetching projects:', error);
        }
    }

    function renderProjects(projects) {
        const gallery = document.querySelector('.portfolio-gallery');
        if (!gallery) return;
        gallery.innerHTML = '';
        projects.forEach(project => {
            const item = document.createElement('div');
            item.className = 'portfolio-item';
            item.innerHTML = `
                <img src="${project.image_url}" alt="${project.title}">
                <div class="portfolio-item-info">
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                </div>
            `;
            gallery.appendChild(item);
        });
    }

    // --- Video Production Assistance ---
    const videoProductionBtn = document.getElementById('video-production-btn');
    if (videoProductionBtn) {
        videoProductionBtn.addEventListener('click', async () => {
            const input = document.getElementById('video-production-input');
            const responseContainer = document.getElementById('video-production-response');
            const apiKey = getApiKey("Please enter your API key to use the Video Producer:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/video/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the video producer');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Create Project ---
    const createProjectBtn = document.getElementById('create-project-btn');
    if (createProjectBtn) {
        createProjectBtn.addEventListener('click', async () => {
            const titleInput = document.getElementById('project-title-input');
            const descriptionInput = document.getElementById('project-description-input');
            const responseContainer = document.getElementById('create-project-response');
            const apiKey = getApiKey("Please enter your API key to create a project:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required to create a project.';
                return;
            }

            try {
                const response = await fetch('/api/v1/projects', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        title: titleInput.value,
                        description: descriptionInput.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to create project');
                }

                const newProject = await response.json();
                responseContainer.textContent = `Project "${newProject.title}" created successfully!`;
                titleInput.value = '';
                descriptionInput.value = '';
                fetchProjects(); // Refresh the portfolio
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Domain Codex Assistance ---
    const domainCodexBtn = document.getElementById('domain-codex-btn');
    if (domainCodexBtn) {
        domainCodexBtn.addEventListener('click', async () => {
            const input = document.getElementById('domain-codex-input');
            const responseContainer = document.getElementById('domain-codex-response');
            const apiKey = getApiKey("Please enter your API key to use the Domain Codex Designer:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/domain-codex/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the domain codex designer');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Data Science & Stewardship Assistance ---
    const dataScienceStewardshipBtn = document.getElementById('data-science-stewardship-btn');
    if (dataScienceStewardshipBtn) {
        dataScienceStewardshipBtn.addEventListener('click', async () => {
            const input = document.getElementById('data-science-stewardship-input');
            const responseContainer = document.getElementById('data-science-stewardship-response');
            const apiKey = getApiKey("Please enter your API key to use the Data Science, Steward & DPO Assistant:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/data-science-stewardship/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the data science & stewardship assistant');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Document Specialist ---
    const documentSpecialistBtn = document.getElementById('document-specialist-btn');
    if (documentSpecialistBtn) {
        documentSpecialistBtn.addEventListener('click', async () => {
            const input = document.getElementById('document-specialist-input');
            const responseContainer = document.getElementById('document-specialist-response');
            const apiKey = getApiKey("Please enter your API key to use the Document Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/assistance/document', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the document specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Promote Startup ---
    const promoteStartupBtn = document.getElementById('promote-startup-btn');
    if (promoteStartupBtn) {
        promoteStartupBtn.addEventListener('click', async () => {
            const descriptionInput = document.getElementById('startup-description-input');
            const responseContainer = document.getElementById('promote-startup-response');
            const apiKey = getApiKey("Please enter your API key to generate a promotion:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required to generate a promotion.';
                return;
            }

            try {
                const response = await fetch('/api/v1/promotions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        description: descriptionInput.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to generate promotion');
                }

                const promotion = await response.json();
                responseContainer.textContent = promotion.promotion_text;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Sciences Educator ---
    const sciencesEducatorBtn = document.getElementById('sciences-educator-btn');
    if (sciencesEducatorBtn) {
        sciencesEducatorBtn.addEventListener('click', async () => {
            const input = document.getElementById('sciences-educator-input');
            const responseContainer = document.getElementById('sciences-educator-response');
            const apiKey = getApiKey("Please enter your API key to use the Sciences Educator:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/sciences/educator', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the educator');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Music Instrumentalist ---
    const musicInstrumentalistBtn = document.getElementById('music-instrumentalist-btn');
    if (musicInstrumentalistBtn) {
        musicInstrumentalistBtn.addEventListener('click', async () => {
            const input = document.getElementById('music-instrumentalist-input');
            const responseContainer = document.getElementById('music-instrumentalist-response');
            const apiKey = getApiKey("Please enter your API key to use the Music Instrumentalist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/play/music', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the music instrumentalist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Geometry Assistant ---
    const geometryAssistantBtn = document.getElementById('geometry-assistant-btn');
    if (geometryAssistantBtn) {
        geometryAssistantBtn.addEventListener('click', async () => {
            const input = document.getElementById('geometry-assistant-input');
            const responseContainer = document.getElementById('geometry-assistant-response');
            const apiKey = getApiKey("Please enter your API key to use the Geometry Assistant:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/assistance/geometry', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the geometry assistant');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Cartography Assistant ---
    const cartographyAssistantBtn = document.getElementById('cartography-assistant-btn');
    if (cartographyAssistantBtn) {
        cartographyAssistantBtn.addEventListener('click', async () => {
            const input = document.getElementById('cartography-assistant-input');
            const responseContainer = document.getElementById('cartography-assistant-response');
            const apiKey = getApiKey("Please enter your API key to use the Cartography Assistant:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/assistance/cartography', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the cartography assistant');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Business Plan Creator ---
    const businessPlanBtn = document.getElementById('business-plan-btn');
    if (businessPlanBtn) {
        businessPlanBtn.addEventListener('click', async () => {
            const input = document.getElementById('business-plan-input');
            const responseContainer = document.getElementById('business-plan-response');
            const apiKey = getApiKey("Please enter your API key to use the Business Plan Creator:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/business/plan', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the business plan creator');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Investigation Role ---
    const investigationRoleBtn = document.getElementById('investigation-role-btn');
    if (investigationRoleBtn) {
        investigationRoleBtn.addEventListener('click', async () => {
            const input = document.getElementById('investigation-role-input');
            const responseContainer = document.getElementById('investigation-role-response');
            const apiKey = getApiKey("Please enter your API key to use the Investigation Role:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/investigation/security', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the investigation role');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Military Assistance ---
    const militaryAssistanceBtn = document.getElementById('military-assistance-btn');
    if (militaryAssistanceBtn) {
        militaryAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('military-assistance-input');
            const responseContainer = document.getElementById('military-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the Military Services Assistance:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/military/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the military assistance role');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Podcast Assistance ---
    const podcastAssistanceBtn = document.getElementById('podcast-assistance-btn');
    if (podcastAssistanceBtn) {
        podcastAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('podcast-assistance-input');
            const responseContainer = document.getElementById('podcast-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the Podcast & Business Podcast Role:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/podcast/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the podcast assistance role');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Supply Chain Assistance ---
    const supplyChainAssistanceBtn = document.getElementById('supply-chain-assistance-btn');
    if (supplyChainAssistanceBtn) {
        supplyChainAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('supply-chain-assistance-input');
            const responseContainer = document.getElementById('supply-chain-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the Supply Chain Consultant:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/supply-chain/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the supply chain consultant');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Logistics Assistance ---
    const logisticsAssistanceBtn = document.getElementById('logistics-assistance-btn');
    if (logisticsAssistanceBtn) {
        logisticsAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('logistics-assistance-input');
            const responseContainer = document.getElementById('logistics-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the Logistics & Transportation Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/logistics/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the logistics specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Data Engineering Assistance ---
    const dataEngineeringAssistanceBtn = document.getElementById('data-engineering-assistance-btn');
    if (dataEngineeringAssistanceBtn) {
        dataEngineeringAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('data-engineering-assistance-input');
            const responseContainer = document.getElementById('data-engineering-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the Data Engineering Expert:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/data-engineering/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the data engineering expert');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- IA & Data Engineering Assistance ---
    const iaDataEngineeringAssistanceBtn = document.getElementById('ia-data-engineering-assistance-btn');
    if (iaDataEngineeringAssistanceBtn) {
        iaDataEngineeringAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('ia-data-engineering-assistance-input');
            const responseContainer = document.getElementById('ia-data-engineering-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the IA & Data Engineering Expert:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/ia-data-engineering/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the IA & data engineering expert');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Data Lab & Data Center Assistance ---
    const dataLabCenterAssistanceBtn = document.getElementById('data-lab-center-assistance-btn');
    if (dataLabCenterAssistanceBtn) {
        dataLabCenterAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('data-lab-center-assistance-input');
            const responseContainer = document.getElementById('data-lab-center-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the Data Lab & Data Center Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/data-lab-center/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the data lab & data center specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Incoterms Assistance ---
    const incotermsAssistanceBtn = document.getElementById('incoterms-assistance-btn');
    if (incotermsAssistanceBtn) {
        incotermsAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('incoterms-assistance-input');
            const responseContainer = document.getElementById('incoterms-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the Incoterms Expert:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/incoterms/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the incoterms expert');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- E-commerce Assistance ---
    const ecommerceAssistanceBtn = document.getElementById('ecommerce-assistance-btn');
    if (ecommerceAssistanceBtn) {
        ecommerceAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('ecommerce-assistance-input');
            const responseContainer = document.getElementById('ecommerce-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the E-commerce & Website Manager:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/ecommerce/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the e-commerce assistant');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Government Assistance ---
    const governmentAssistanceBtn = document.getElementById('government-assistance-btn');
    if (governmentAssistanceBtn) {
        governmentAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('government-assistance-input');
            const responseContainer = document.getElementById('government-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the Government Public Administrator:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/government/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the government assistant');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Biotech Assistance ---
    const biotechAssistanceBtn = document.getElementById('biotech-assistance-btn');
    if (biotechAssistanceBtn) {
        biotechAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('biotech-assistance-input');
            const responseContainer = document.getElementById('biotech-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the Biotech Development Role:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/biotech/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the biotech development role');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Legal Assistance ---
    const legalAssistanceBtn = document.getElementById('legal-assistance-btn');
    if (legalAssistanceBtn) {
        legalAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('legal-assistance-input');
            const responseContainer = document.getElementById('legal-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the Legal & Human Rights Assistant:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/legal/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the legal assistant');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Fintech Assistance ---
    const fintechAssistanceBtn = document.getElementById('fintech-assistance-btn');
    if (fintechAssistanceBtn) {
        fintechAssistanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('fintech-assistance-input');
            const responseContainer = document.getElementById('fintech-assistance-response');
            const apiKey = getApiKey("Please enter your API key to use the Fintech & Banking Strategist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/fintech/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the fintech strategist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Music Production ---
    const musicProductionBtn = document.getElementById('music-production-btn');
    if (musicProductionBtn) {
        musicProductionBtn.addEventListener('click', async () => {
            const input = document.getElementById('music-production-input');
            const responseContainer = document.getElementById('music-production-response');
            const apiKey = getApiKey("Please enter your API key to use the Music Production & Promotion role:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/music/production', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the music production role');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Aerospace & Automotive Assistance ---
    const aerospaceAutomotiveBtn = document.getElementById('aerospace-automotive-btn');
    if (aerospaceAutomotiveBtn) {
        aerospaceAutomotiveBtn.addEventListener('click', async () => {
            const input = document.getElementById('aerospace-automotive-input');
            const responseContainer = document.getElementById('aerospace-automotive-response');
            const apiKey = getApiKey("Please enter your API key to use the Aerospace & Automotive Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/aerospace-automotive/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the aerospace & automotive specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Logo & Thumbnail Creator ---
    const logoThumbnailBtn = document.getElementById('logo-thumbnail-btn');
    if (logoThumbnailBtn) {
        logoThumbnailBtn.addEventListener('click', async () => {
            const input = document.getElementById('logo-thumbnail-input');
            const responseContainer = document.getElementById('logo-thumbnail-response');
            const apiKey = getApiKey("Please enter your API key to use the Logo & Thumbnail Creator:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/logo-thumbnail/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the logo & thumbnail creator');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Automatic Learning Assistance ---
    const automaticLearningBtn = document.getElementById('automatic-learning-btn');
    if (automaticLearningBtn) {
        automaticLearningBtn.addEventListener('click', async () => {
            const input = document.getElementById('automatic-learning-input');
            const responseContainer = document.getElementById('automatic-learning-response');
            const apiKey = getApiKey("Please enter your API key to use the Automatic Learning Role:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/automatic-learning/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the automatic learning assistant');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Malware Defense Assistance ---
    const malwareDefenseBtn = document.getElementById('malware-defense-btn');
    if (malwareDefenseBtn) {
        malwareDefenseBtn.addEventListener('click', async () => {
            const input = document.getElementById('malware-defense-input');
            const responseContainer = document.getElementById('malware-defense-response');
            const apiKey = getApiKey("Please enter your API key to use the Malware Defender:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/malware-defense/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the malware defender');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Fake Content Verification ---
    const fakeContentBtn = document.getElementById('fake-content-btn');
    if (fakeContentBtn) {
        fakeContentBtn.addEventListener('click', async () => {
            const input = document.getElementById('fake-content-input');
            const responseContainer = document.getElementById('fake-content-response');
            const apiKey = getApiKey("Please enter your API key to use the AI Content & Fake News Verifier:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/fake-content/verification', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the verifier');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Computer Vision Assistance ---
    const computerVisionBtn = document.getElementById('computer-vision-btn');
    if (computerVisionBtn) {
        computerVisionBtn.addEventListener('click', async () => {
            const input = document.getElementById('computer-vision-input');
            const responseContainer = document.getElementById('computer-vision-response');
            const apiKey = getApiKey("Please enter your API key to use the Computer Vision Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/computer-vision/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the computer vision specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- IA Researcher Assistance ---
    const iaResearcherBtn = document.getElementById('ia-researcher-btn');
    if (iaResearcherBtn) {
        iaResearcherBtn.addEventListener('click', async () => {
            const input = document.getElementById('ia-researcher-input');
            const responseContainer = document.getElementById('ia-researcher-response');
            const apiKey = getApiKey("Please enter your API key to use the IA Researcher:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/ia-researcher/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the IA researcher');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- eSports Assistance ---
    const esportsBtn = document.getElementById('esports-btn');
    if (esportsBtn) {
        esportsBtn.addEventListener('click', async () => {
            const input = document.getElementById('esports-input');
            const responseContainer = document.getElementById('esports-response');
            const apiKey = getApiKey("Please enter your API key to use the eSports Development & Assistance:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/esports/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the eSports assistant');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Dermatology Assistance ---
    const dermatologyBtn = document.getElementById('dermatology-btn');
    if (dermatologyBtn) {
        dermatologyBtn.addEventListener('click', async () => {
            const input = document.getElementById('dermatology-input');
            const responseContainer = document.getElementById('dermatology-response');
            const apiKey = getApiKey("Please enter your API key to use the AI Dermatology Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/dermatology/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the dermatology specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Microsoft Ignite Assistance ---
    const microsoftIgniteBtn = document.getElementById('microsoft-ignite-btn');
    if (microsoftIgniteBtn) {
        microsoftIgniteBtn.addEventListener('click', async () => {
            const input = document.getElementById('microsoft-ignite-input');
            const responseContainer = document.getElementById('microsoft-ignite-response');
            const apiKey = getApiKey("Please enter your API key to use the Microsoft Ignite & Azure AI Expert:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/microsoft-ignite/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the Microsoft Ignite expert');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Diagnostic Assistance ---
    const diagnosticBtn = document.getElementById('diagnostic-btn');
    if (diagnosticBtn) {
        diagnosticBtn.addEventListener('click', async () => {
            const input = document.getElementById('diagnostic-input');
            const responseContainer = document.getElementById('diagnostic-response');
            const apiKey = getApiKey("Please enter your API key to use the AI Diagnostic Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/diagnostic/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the diagnostic specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- IT Operations Assistance ---
    const itOperationsBtn = document.getElementById('it-operations-btn');
    if (itOperationsBtn) {
        itOperationsBtn.addEventListener('click', async () => {
            const input = document.getElementById('it-operations-input');
            const responseContainer = document.getElementById('it-operations-response');
            const apiKey = getApiKey("Please enter your API key to use the IT Operations Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/it-operations/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the IT operations specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Maintenance Assistance ---
    const maintenanceBtn = document.getElementById('maintenance-btn');
    if (maintenanceBtn) {
        maintenanceBtn.addEventListener('click', async () => {
            const input = document.getElementById('maintenance-input');
            const responseContainer = document.getElementById('maintenance-response');
            const apiKey = getApiKey("Please enter your API key to use the Software & Hardware Maintenance Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/maintenance/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the maintenance specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Marketing Assistance ---
    const marketingBtn = document.getElementById('marketing-btn');
    if (marketingBtn) {
        marketingBtn.addEventListener('click', async () => {
            const input = document.getElementById('marketing-input');
            const responseContainer = document.getElementById('marketing-response');
            const apiKey = getApiKey("Please enter your API key to use the Digital Marketing & Bot Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/marketing/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the marketing specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Investment & Trading Assistance ---
    const investmentTradingBtn = document.getElementById('investment-trading-btn');
    if (investmentTradingBtn) {
        investmentTradingBtn.addEventListener('click', async () => {
            const input = document.getElementById('investment-trading-input');
            const responseContainer = document.getElementById('investment-trading-response');
            const apiKey = getApiKey("Please enter your API key to use the Investment & Trading Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/investment-trading/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the investment & trading specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Digital Repair Assistance ---
    const digitalRepairBtn = document.getElementById('digital-repair-btn');
    if (digitalRepairBtn) {
        digitalRepairBtn.addEventListener('click', async () => {
            const input = document.getElementById('digital-repair-input');
            const responseContainer = document.getElementById('digital-repair-response');
            const apiKey = getApiKey("Please enter your API key to use the Digital Repair Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/digital-repair/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the digital repair specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- AutoGPT Assistance ---
    const autogptBtn = document.getElementById('autogpt-btn');
    if (autogptBtn) {
        autogptBtn.addEventListener('click', async () => {
            const input = document.getElementById('autogpt-input');
            const responseContainer = document.getElementById('autogpt-response');
            const apiKey = getApiKey("Please enter your API key to use the AutoGPT Agent:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/autogpt/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the AutoGPT agent');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- AutoML Feature Engineering ---
    const automlFeatureEngineeringBtn = document.getElementById('automl-feature-engineering-btn');
    if (automlFeatureEngineeringBtn) {
        automlFeatureEngineeringBtn.addEventListener('click', async () => {
            const input = document.getElementById('automl-feature-engineering-input');
            const responseContainer = document.getElementById('automl-feature-engineering-response');
            const apiKey = getApiKey("Please enter your API key to use the AutoML Feature Engineering Expert:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/automl/feature-engineering', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the AutoML feature engineering expert');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- AutoML Hyperparameter Tuning ---
    const automlHyperparameterTuningBtn = document.getElementById('automl-hyperparameter-tuning-btn');
    if (automlHyperparameterTuningBtn) {
        automlHyperparameterTuningBtn.addEventListener('click', async () => {
            const input = document.getElementById('automl-hyperparameter-tuning-input');
            const responseContainer = document.getElementById('automl-hyperparameter-tuning-response');
            const apiKey = getApiKey("Please enter your API key to use the AutoML Hyperparameter Tuner:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/automl/hyperparameter-tuning', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the AutoML hyperparameter tuner');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- AutoML Model Selection ---
    const automlModelSelectionBtn = document.getElementById('automl-model-selection-btn');
    if (automlModelSelectionBtn) {
        automlModelSelectionBtn.addEventListener('click', async () => {
            const input = document.getElementById('automl-model-selection-input');
            const responseContainer = document.getElementById('automl-model-selection-response');
            const apiKey = getApiKey("Please enter your API key to use the AutoML Model Selector:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/automl/model-selection', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the AutoML model selector');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- AutoML MLOps ---
    const automlMLOpsBtn = document.getElementById('automl-mlops-btn');
    if (automlMLOpsBtn) {
        automlMLOpsBtn.addEventListener('click', async () => {
            const input = document.getElementById('automl-mlops-input');
            const responseContainer = document.getElementById('automl-mlops-response');
            const apiKey = getApiKey("Please enter your API key to use the AutoML MLOps Expert:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/automl/mlops', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the AutoML MLOps expert');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- E-shop Assistance ---
    const eshopBtn = document.getElementById('eshop-btn');
    if (eshopBtn) {
        eshopBtn.addEventListener('click', async () => {
            const input = document.getElementById('eshop-input');
            const responseContainer = document.getElementById('eshop-response');
            const apiKey = getApiKey("Please enter your API key to use the E-shop Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/eshop/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the e-shop specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Global Translator ---
    const translatorBtn = document.getElementById('translator-btn');
    if (translatorBtn) {
        translatorBtn.addEventListener('click', async () => {
            const textInput = document.getElementById('translator-text-input');
            const languageInput = document.getElementById('translator-language-input');
            const responseContainer = document.getElementById('translator-response');
            const apiKey = getApiKey("Please enter your API key to use the Global Translator:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/translate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        text: textInput.value,
                        target_language: languageInput.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the translator');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Cloud Infrastructure Assistance ---
    const cloudInfrastructureBtn = document.getElementById('cloud-infrastructure-btn');
    if (cloudInfrastructureBtn) {
        cloudInfrastructureBtn.addEventListener('click', async () => {
            const input = document.getElementById('cloud-infrastructure-input');
            const responseContainer = document.getElementById('cloud-infrastructure-response');
            const apiKey = getApiKey("Please enter your API key to use the Cloud Infrastructure Architect:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/cloud-infrastructure/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the cloud infrastructure architect');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Llama Intelligence ---
    const llamaIntelligenceBtn = document.getElementById('llama-intelligence-btn');
    if (llamaIntelligenceBtn) {
        llamaIntelligenceBtn.addEventListener('click', async () => {
            const input = document.getElementById('llama-intelligence-input');
            const responseContainer = document.getElementById('llama-intelligence-response');
            const apiKey = getApiKey("Please enter your API key to use the Llama Intelligence Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/llama/intelligence', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from Llama Intelligence');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Llama Guard ---
    const llamaGuardBtn = document.getElementById('llama-guard-btn');
    if (llamaGuardBtn) {
        llamaGuardBtn.addEventListener('click', async () => {
            const input = document.getElementById('llama-guard-input');
            const responseContainer = document.getElementById('llama-guard-response');
            const apiKey = getApiKey("Please enter your API key to use the Llama Guard Safety Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/llama/guard', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from Llama Guard');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- NVIDIA Nemotron ---
    const nemotronBtn = document.getElementById('nvidia-nemotron-btn');
    if (nemotronBtn) {
        nemotronBtn.addEventListener('click', async () => {
            const input = document.getElementById('nvidia-nemotron-input');
            const responseContainer = document.getElementById('nvidia-nemotron-response');
            const apiKey = getApiKey("Please enter your API key to use the Nemotron Reasoning Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/nvidia/nemotron', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from Nemotron');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- NVIDIA Mixtral ---
    const mixtralBtn = document.getElementById('nvidia-mixtral-btn');
    if (mixtralBtn) {
        mixtralBtn.addEventListener('click', async () => {
            const input = document.getElementById('nvidia-mixtral-input');
            const responseContainer = document.getElementById('nvidia-mixtral-response');
            const apiKey = getApiKey("Please enter your API key to use the Mixtral Multilingual Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/nvidia/mixtral', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from Mixtral');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Anthropic Intelligence ---
    const anthropicIntelligenceBtn = document.getElementById('anthropic-intelligence-btn');
    if (anthropicIntelligenceBtn) {
        anthropicIntelligenceBtn.addEventListener('click', async () => {
            const input = document.getElementById('anthropic-intelligence-input');
            const responseContainer = document.getElementById('anthropic-intelligence-response');
            const apiKey = getApiKey("Please enter your API key to use the Claude Intelligence Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/anthropic/intelligence', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from Anthropic Claude');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Psychoanalyst & Dream Interpreter ---
    const psychoanalysisBtn = document.getElementById('psychoanalysis-btn');
    if (psychoanalysisBtn) {
        psychoanalysisBtn.addEventListener('click', async () => {
            const input = document.getElementById('psychoanalysis-input');
            const responseContainer = document.getElementById('psychoanalysis-response');
            const apiKey = getApiKey("Please enter your API key to use the Psychoanalyst & Dream Interpreter:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/psychoanalysis/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the Psychoanalyst');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Xero Specialist ---
    const xeroBtn = document.getElementById('xero-btn');
    if (xeroBtn) {
        xeroBtn.addEventListener('click', async () => {
            const input = document.getElementById('xero-input');
            const responseContainer = document.getElementById('xero-response');
            const apiKey = getApiKey("Please enter your API key to use the Xero Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/xero/assistance', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the Xero Specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- OS Hardening Specialist ---
    const osHardeningBtn = document.getElementById('os-hardening-btn');
    if (osHardeningBtn) {
        osHardeningBtn.addEventListener('click', async () => {
            const input = document.getElementById('os-hardening-input');
            const responseContainer = document.getElementById('os-hardening-response');
            const apiKey = getApiKey("Please enter your API key to use the OS Hardening Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/security/os-hardening', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from the OS hardening specialist');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }

    // --- Anthropic Coding ---
    const anthropicCodingBtn = document.getElementById('anthropic-coding-btn');
    if (anthropicCodingBtn) {
        anthropicCodingBtn.addEventListener('click', async () => {
            const input = document.getElementById('anthropic-coding-input');
            const responseContainer = document.getElementById('anthropic-coding-response');
            const apiKey = getApiKey("Please enter your API key to use the Claude Coding Specialist:");

            if (!apiKey) {
                responseContainer.textContent = 'API key is required.';
                return;
            }

            try {
                const response = await fetch('/api/v1/anthropic/coding', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': apiKey
                    },
                    body: JSON.stringify({
                        prompt: input.value
                    })
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to get a response from Anthropic Claude');
                }

                const result = await response.json();
                responseContainer.textContent = result.message;
            } catch (error) {
                responseContainer.textContent = `Error: ${error.message}`;
            }
        });
    }
});
