import os
import sys
from pathlib import Path

PACKAGE_PATH = Path(os.path.abspath(__file__)).parent
PROJECT_PATH = PACKAGE_PATH.parent

sys.path.append(str(PROJECT_PATH))

from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def create_complex_network() -> nx.DiGraph:
    """
    Create an extremely complex business ecosystem with realistic industry relationships,
    multiple geographical regions, supply chains, and intricate interdependencies.

    Network Features:
    - 75+ companies across 12 major industry sectors
    - Multi-tier supply chains with upstream/downstream relationships
    - Regional hubs and cross-regional dependencies
    - Financial institutions serving multiple sectors
    - Technology companies providing cross-industry services
    - Complex overlapping cycles of various lengths (3-8 nodes)
    - Realistic debt amounts based on relationship types and company sizes
    """
    G = nx.DiGraph()

    # Define comprehensive industry sectors with realistic company structures
    sectors = {
        "manufacturing": {
            "heavy_industry": [
                "GlobalSteelCorp",
                "AluminiumWorks",
                "ChemicalGiant",
                "PetrochemIndustries",
            ],
            "automotive": [
                "AutoManufacturing",
                "EngineWorks",
                "TireProduction",
                "AutoElectronics",
                "CarBodyworks",
            ],
            "aerospace": [
                "AerospaceDefense",
                "AircraftParts",
                "SpaceComponents",
                "AvionicsSystem",
            ],
            "machinery": [
                "IndustrialMachinery",
                "RoboticsInc",
                "ToolManufacturing",
                "PrecisionEquipment",
            ],
        },
        "retail": {
            "mass_retail": [
                "MegaRetailChain",
                "GlobalSupermarket",
                "DiscountStores",
                "WarehouseClub",
            ],
            "specialty": [
                "LuxuryFashion",
                "SportingGoods",
                "ElectronicsRetail",
                "HomeImprovement",
            ],
            "ecommerce": [
                "OnlineMarketplace",
                "EcommercePlatform",
                "DigitalRetail",
                "DirectConsumer",
            ],
        },
        "technology": {
            "software": [
                "EnterpriseSoftware",
                "CloudSolutions",
                "CybersecurityFirm",
                "DataAnalyticsCorp",
            ],
            "hardware": [
                "SemiconductorFab",
                "ComputerManufacturing",
                "NetworkEquipment",
                "MobileDevices",
            ],
            "ai_ml": [
                "ArtificialIntelligence",
                "MachineLearning",
                "ComputerVision",
                "NaturalLanguageAI",
            ],
        },
        "financial": {
            "banking": ["GlobalBank", "RegionalBank", "InvestmentBank", "CreditUnion"],
            "insurance": [
                "LifeInsurance",
                "PropertyInsurance",
                "HealthInsurance",
                "ReinsuranceCorp",
            ],
            "investment": [
                "HedgeFund",
                "PrivateEquity",
                "VentureCapital",
                "AssetManagement",
            ],
            "fintech": [
                "PaymentProcessor",
                "CryptoCurrency",
                "LendingPlatform",
                "InsurTech",
            ],
        },
        "energy": {
            "oil_gas": [
                "OilMajor",
                "NaturalGasDistributor",
                "RefineryOperations",
                "PetroleumServices",
            ],
            "renewable": [
                "SolarEnergy",
                "WindPower",
                "HydroElectric",
                "GeothermalEnergy",
            ],
            "utilities": [
                "ElectricUtility",
                "WaterUtility",
                "PowerGeneration",
                "EnergyTrading",
            ],
        },
        "healthcare": {
            "pharma": [
                "PharmaceuticalGiant",
                "BiotechFirm",
                "GenericDrugs",
                "VaccineManufacturer",
            ],
            "medical_devices": [
                "MedicalEquipment",
                "DiagnosticDevices",
                "SurgicalInstruments",
                "HealthTech",
            ],
            "services": [
                "HospitalChain",
                "ClinicalLabs",
                "HealthcareIT",
                "TelemedicineCorp",
            ],
        },
        "telecommunications": {
            "telecom": [
                "TelecomGiant",
                "WirelessCarrier",
                "InternetProvider",
                "SatelliteComm",
            ],
            "media": [
                "MediaConglomerate",
                "StreamingService",
                "BroadcastNetwork",
                "ContentProduction",
            ],
        },
        "transportation": {
            "logistics": [
                "GlobalLogistics",
                "FreightForwarder",
                "SupplyChainMgmt",
                "LastMileDelivery",
            ],
            "airlines": [
                "MajorAirline",
                "CargoAirline",
                "RegionalCarrier",
                "AircraftLeasing",
            ],
            "shipping": [
                "ContainerShipping",
                "BulkCarrier",
                "PortOperations",
                "MarineServices",
            ],
        },
        "real_estate": {
            "development": [
                "RealEstateDeveloper",
                "CommercialBuilder",
                "ResidentialBuilder",
                "InfrastructureFirm",
            ],
            "investment": [
                "RealEstateInvestment",
                "PropertyManagement",
                "REITCorporation",
                "LandDevelopment",
            ],
        },
        "agriculture": {
            "farming": [
                "AgricultureCorp",
                "LivestockRanch",
                "CropProduction",
                "OrganicFarms",
            ],
            "food_processing": [
                "FoodProcessing",
                "BeverageCompany",
                "MeatPacking",
                "DairyProcessing",
            ],
        },
        "materials": {
            "mining": [
                "MiningCorporation",
                "PreciousMetals",
                "CoalMining",
                "RareEarthElements",
            ],
            "construction": [
                "CementCompany",
                "ConstructionMaterials",
                "LumberMill",
                "GlassManufacturing",
            ],
        },
        "services": {
            "consulting": [
                "ManagementConsulting",
                "TechConsulting",
                "FinancialAdvisory",
                "StrategyFirm",
            ],
            "professional": [
                "LegalServices",
                "AccountingFirm",
                "ArchitecturalServices",
                "EngineeringConsult",
            ],
            "outsourcing": [
                "BusinessProcessOutsourcing",
                "ITOutsourcing",
                "CallCenter",
                "DataEntry",
            ],
        },
    }

    # Flatten company structure and create mappings
    all_companies = []
    company_to_sector = {}
    company_to_subsector = {}
    sector_companies = defaultdict(list)

    for sector, subsectors in sectors.items():
        for subsector, companies in subsectors.items():
            all_companies.extend(companies)
            sector_companies[sector].extend(companies)
            for company in companies:
                company_to_sector[company] = sector
                company_to_subsector[company] = subsector

    # Add all nodes with attributes
    for company in all_companies:
        G.add_node(
            company,
            sector=company_to_sector[company],
            subsector=company_to_subsector[company],
        )

    # Define complex debt amount ranges by relationship type and company characteristics
    debt_ranges = {
        "mega_contract": (500000, 2000000),  # Major B2B contracts
        "supply_chain_tier1": (200000, 800000),  # Direct suppliers
        "supply_chain_tier2": (50000, 300000),  # Secondary suppliers
        "financial_services": (100000, 1000000),  # Banking/Insurance
        "technology_services": (75000, 400000),  # IT/Software services
        "consulting_services": (25000, 200000),  # Professional services
        "real_estate_lease": (80000, 500000),  # Property leases/purchases
        "utility_services": (30000, 150000),  # Energy/Utilities
        "logistics_services": (40000, 250000),  # Transportation/Logistics
        "intra_sector": (20000, 150000),  # Within same sector
        "cross_sector": (15000, 100000),  # General cross-sector
        "startup_funding": (100000, 500000),  # VC/PE investments
        "commodity_trading": (300000, 1500000),  # Raw materials
        "licensing_royalty": (10000, 80000),  # IP licensing
    }

    def add_debt_edge(
        debtor: str,
        creditor: str,
        relationship_type: str,
        multiplier: float = 1.0,
        description: str = "",
    ):
        """Add a debt edge with appropriate amount based on relationship type"""
        min_debt, max_debt = debt_ranges[relationship_type]
        amount = np.random.uniform(min_debt, max_debt) * multiplier
        G.add_edge(
            debtor,
            creditor,
            amount=amount,
            relationship=relationship_type,
            description=description,
        )

    # 1. CREATE MULTI-TIER SUPPLY CHAINS WITH COMPLEX DEPENDENCIES

    # Automotive Supply Chain (Complex 4-tier structure)
    automotive_chain = {
        "tier1": ["AutoManufacturing", "EngineWorks", "TireProduction"],
        "tier2": [
            "AutoElectronics",
            "CarBodyworks",
            "GlobalSteelCorp",
            "AluminiumWorks",
        ],
        "tier3": ["ChemicalGiant", "PrecisionEquipment", "RoboticsInc"],
        "tier4": ["MiningCorporation", "RareEarthElements", "PetrochemIndustries"],
    }

    # Tier 1 to OEMs and customers
    add_debt_edge(
        "MegaRetailChain",
        "AutoManufacturing",
        "mega_contract",
        1.5,
        "Fleet vehicle purchase",
    )
    add_debt_edge(
        "GlobalLogistics",
        "AutoManufacturing",
        "mega_contract",
        1.2,
        "Commercial vehicles",
    )

    # Tier 2 to Tier 1
    for tier1_company in automotive_chain["tier1"]:
        for tier2_company in automotive_chain["tier2"][:2]:  # Limit connections
            add_debt_edge(
                tier1_company,
                tier2_company,
                "supply_chain_tier1",
                1.0,
                f"{tier2_company} components",
            )

    # Tier 3 to Tier 2
    for tier2_company in automotive_chain["tier2"]:
        for tier3_company in automotive_chain["tier3"][:2]:
            add_debt_edge(
                tier2_company,
                tier3_company,
                "supply_chain_tier2",
                1.0,
                f"{tier3_company} materials",
            )

    # Tier 4 to Tier 3
    for tier3_company in automotive_chain["tier3"]:
        for tier4_company in automotive_chain["tier4"][:2]:
            add_debt_edge(
                tier3_company,
                tier4_company,
                "commodity_trading",
                1.0,
                f"Raw materials from {tier4_company}",
            )

    # Technology Supply Chain (Software/Hardware integration)
    tech_ecosystem = [
        (
            "OnlineMarketplace",
            "CloudSolutions",
            "technology_services",
            "Cloud infrastructure",
        ),
        (
            "CloudSolutions",
            "SemiconductorFab",
            "supply_chain_tier1",
            "Server processors",
        ),
        (
            "SemiconductorFab",
            "RareEarthElements",
            "commodity_trading",
            "Rare earth minerals",
        ),
        (
            "EnterpriseSoftware",
            "ArtificialIntelligence",
            "technology_services",
            "AI integration",
        ),
        (
            "ArtificialIntelligence",
            "ComputerVision",
            "technology_services",
            "Vision algorithms",
        ),
        ("ComputerVision", "CybersecurityFirm", "cross_sector", "Security analytics"),
        (
            "CybersecurityFirm",
            "DataAnalyticsCorp",
            "technology_services",
            "Threat intelligence",
        ),
        (
            "DataAnalyticsCorp",
            "CloudSolutions",
            "technology_services",
            "Analytics platform",
        ),
    ]

    for debtor, creditor, rel_type, desc in tech_ecosystem:
        add_debt_edge(debtor, creditor, rel_type, 1.0, desc)

    # Energy Sector Complex Chain
    energy_chain = [
        ("ElectricUtility", "OilMajor", "commodity_trading", "Petroleum products"),
        (
            "OilMajor",
            "RefineryOperations",
            "supply_chain_tier1",
            "Crude oil processing",
        ),
        (
            "RefineryOperations",
            "PetroleumServices",
            "supply_chain_tier2",
            "Refinery services",
        ),
        ("ElectricUtility", "SolarEnergy", "mega_contract", "Solar power purchase"),
        ("SolarEnergy", "SemiconductorFab", "supply_chain_tier1", "Solar panels"),
        ("WindPower", "GlobalSteelCorp", "supply_chain_tier1", "Wind turbines"),
        (
            "PowerGeneration",
            "NaturalGasDistributor",
            "commodity_trading",
            "Natural gas",
        ),
        (
            "EnergyTrading",
            "ElectricUtility",
            "financial_services",
            "Energy derivatives",
        ),
    ]

    for debtor, creditor, rel_type, desc in energy_chain:
        add_debt_edge(debtor, creditor, rel_type, 1.2, desc)

    # 2. CREATE FINANCIAL SERVICES NETWORKS (Banks serving all sectors)

    major_banks = ["GlobalBank", "RegionalBank", "InvestmentBank"]
    high_capital_companies = [
        "MegaRetailChain",
        "AutoManufacturing",
        "OilMajor",
        "PharmaceuticalGiant",
        "TelecomGiant",
        "AerospaceDefense",
        "GlobalLogistics",
        "RealEstateDeveloper",
    ]

    # Banking relationships
    for bank in major_banks:
        for company in high_capital_companies[:5]:  # Limit connections per bank
            add_debt_edge(
                company,
                bank,
                "financial_services",
                1.5,
                f"Corporate banking with {bank}",
            )

    # Insurance networks
    insurance_companies = ["LifeInsurance", "PropertyInsurance", "HealthInsurance"]
    for insurance in insurance_companies:
        for company in high_capital_companies[2:7]:
            add_debt_edge(
                company,
                insurance,
                "financial_services",
                0.8,
                f"Insurance premiums to {insurance}",
            )

    # Investment and private equity
    investment_firms = ["HedgeFund", "PrivateEquity", "VentureCapital"]
    growth_companies = [
        "EcommercePlatform",
        "ArtificialIntelligence",
        "BiotechFirm",
        "CryptoCurrency",
        "InsurTech",
        "HealthTech",
        "CleanEnergy",
    ]

    for i, investment_firm in enumerate(investment_firms):
        for company in growth_companies[i * 2 : (i + 1) * 3]:  # Distribute investments
            add_debt_edge(
                investment_firm,
                company,
                "startup_funding",
                2.0,
                f"Investment from {investment_firm}",
            )

    # 3. CREATE TECHNOLOGY SERVICE OVERLAYS (Tech companies serving all sectors)

    tech_service_providers = [
        "EnterpriseSoftware",
        "CloudSolutions",
        "CybersecurityFirm",
        "DataAnalyticsCorp",
    ]

    # Technology services across all sectors
    all_non_tech_companies = [
        c for c in all_companies if company_to_sector[c] not in ["technology"]
    ]

    for tech_provider in tech_service_providers:
        # Each tech provider serves 8-12 companies across different sectors
        served_companies = np.random.choice(
            all_non_tech_companies, size=10, replace=False
        )
        for company in served_companies:
            add_debt_edge(
                company,
                tech_provider,
                "technology_services",
                0.9,
                f"IT services from {tech_provider}",
            )

    # 4. CREATE CONSULTING AND PROFESSIONAL SERVICES NETWORKS

    consulting_firms = [
        "ManagementConsulting",
        "TechConsulting",
        "FinancialAdvisory",
        "StrategyFirm",
    ]
    professional_services = [
        "LegalServices",
        "AccountingFirm",
        "ArchitecturalServices",
        "EngineeringConsult",
    ]

    large_corporations = [
        "MegaRetailChain",
        "AutoManufacturing",
        "PharmaceuticalGiant",
        "TelecomGiant",
        "GlobalBank",
        "OilMajor",
        "AerospaceDefense",
        "RealEstateDeveloper",
    ]

    # Consulting relationships
    for consulting_firm in consulting_firms:
        for corp in large_corporations[:6]:
            add_debt_edge(
                corp,
                consulting_firm,
                "consulting_services",
                1.0,
                f"Strategic consulting from {consulting_firm}",
            )

    # Professional services
    for service_firm in professional_services:
        for corp in large_corporations[2:]:
            add_debt_edge(
                corp,
                service_firm,
                "consulting_services",
                0.7,
                f"Professional services from {service_firm}",
            )

    # 5. CREATE COMPLEX OVERLAPPING CYCLES

    # Mega Hub Cycle (Major players from different sectors)
    mega_hub_cycle = [
        (
            "MegaRetailChain",
            "GlobalLogistics",
            "logistics_services",
            "Supply chain logistics",
        ),
        ("GlobalLogistics", "AutoManufacturing", "mega_contract", "Fleet vehicles"),
        ("AutoManufacturing", "GlobalBank", "financial_services", "Corporate banking"),
        (
            "GlobalBank",
            "RealEstateDeveloper",
            "financial_services",
            "Construction loans",
        ),
        (
            "RealEstateDeveloper",
            "ConstructionMaterials",
            "supply_chain_tier1",
            "Building materials",
        ),
        (
            "ConstructionMaterials",
            "MiningCorporation",
            "commodity_trading",
            "Raw materials",
        ),
        ("MiningCorporation", "GlobalSteelCorp", "commodity_trading", "Iron ore"),
        (
            "GlobalSteelCorp",
            "MegaRetailChain",
            "supply_chain_tier2",
            "Steel products retail",
        ),
    ]

    for debtor, creditor, rel_type, desc in mega_hub_cycle:
        add_debt_edge(debtor, creditor, rel_type, 1.8, desc)

    # Healthcare Ecosystem Cycle
    healthcare_cycle = [
        (
            "HospitalChain",
            "PharmaceuticalGiant",
            "supply_chain_tier1",
            "Pharmaceutical supplies",
        ),
        (
            "PharmaceuticalGiant",
            "BiotechFirm",
            "technology_services",
            "R&D collaboration",
        ),
        ("BiotechFirm", "VentureCapital", "startup_funding", "Biotech funding"),
        (
            "VentureCapital",
            "HealthTech",
            "startup_funding",
            "Digital health investment",
        ),
        ("HealthTech", "CloudSolutions", "technology_services", "Cloud infrastructure"),
        (
            "CloudSolutions",
            "HospitalChain",
            "technology_services",
            "Hospital IT systems",
        ),
    ]

    for debtor, creditor, rel_type, desc in healthcare_cycle:
        add_debt_edge(debtor, creditor, rel_type, 1.3, desc)

    # Media and Entertainment Complex
    media_entertainment_cycle = [
        ("StreamingService", "ContentProduction", "mega_contract", "Original content"),
        (
            "ContentProduction",
            "MediaConglomerate",
            "licensing_royalty",
            "Content licensing",
        ),
        (
            "MediaConglomerate",
            "TelecomGiant",
            "technology_services",
            "Broadcasting infrastructure",
        ),
        ("TelecomGiant", "SatelliteComm", "technology_services", "Satellite services"),
        (
            "SatelliteComm",
            "AerospaceDefense",
            "supply_chain_tier1",
            "Satellite manufacturing",
        ),
        (
            "AerospaceDefense",
            "StreamingService",
            "technology_services",
            "Satellite capacity",
        ),
    ]

    for debtor, creditor, rel_type, desc in media_entertainment_cycle:
        add_debt_edge(debtor, creditor, rel_type, 1.1, desc)

    # 6. CREATE REGIONAL AND GLOBAL SUPPLY CHAINS

    # Agriculture to Food Processing Chain
    agri_food_chain = [
        (
            "MegaRetailChain",
            "FoodProcessing",
            "supply_chain_tier1",
            "Processed food products",
        ),
        (
            "FoodProcessing",
            "AgricultureCorp",
            "supply_chain_tier1",
            "Agricultural products",
        ),
        (
            "AgricultureCorp",
            "ChemicalGiant",
            "supply_chain_tier2",
            "Agricultural chemicals",
        ),
        (
            "BeverageCompany",
            "AgricultureCorp",
            "supply_chain_tier1",
            "Raw beverage ingredients",
        ),
        ("DairyProcessing", "LivestockRanch", "supply_chain_tier1", "Dairy products"),
        ("MeatPacking", "LivestockRanch", "supply_chain_tier1", "Livestock"),
        ("GlobalSupermarket", "FoodProcessing", "supply_chain_tier1", "Food products"),
        ("GlobalSupermarket", "BeverageCompany", "supply_chain_tier1", "Beverages"),
    ]

    for debtor, creditor, rel_type, desc in agri_food_chain:
        add_debt_edge(debtor, creditor, rel_type, 1.0, desc)

    # Real Estate and Construction Ecosystem
    real_estate_construction = [
        (
            "RealEstateDeveloper",
            "CommercialBuilder",
            "mega_contract",
            "Construction services",
        ),
        (
            "CommercialBuilder",
            "ConstructionMaterials",
            "supply_chain_tier1",
            "Building materials",
        ),
        (
            "CommercialBuilder",
            "ArchitecturalServices",
            "consulting_services",
            "Design services",
        ),
        (
            "ConstructionMaterials",
            "CementCompany",
            "supply_chain_tier2",
            "Cement products",
        ),
        (
            "ConstructionMaterials",
            "LumberMill",
            "supply_chain_tier2",
            "Lumber products",
        ),
        (
            "CementCompany",
            "MiningCorporation",
            "commodity_trading",
            "Limestone and aggregates",
        ),
        (
            "PropertyManagement",
            "RealEstateDeveloper",
            "consulting_services",
            "Property management",
        ),
        (
            "RealEstateInvestment",
            "PropertyManagement",
            "financial_services",
            "Investment management",
        ),
    ]

    for debtor, creditor, rel_type, desc in real_estate_construction:
        add_debt_edge(debtor, creditor, rel_type, 1.2, desc)

    # 7. CREATE ADDITIONAL OVERLAPPING CYCLES AND HUB RELATIONSHIPS

    # Fintech and Traditional Finance Integration
    fintech_traditional = [
        ("PaymentProcessor", "GlobalBank", "financial_services", "Payment processing"),
        ("CryptoCurrency", "InvestmentBank", "financial_services", "Crypto trading"),
        ("LendingPlatform", "RegionalBank", "financial_services", "Loan origination"),
        (
            "InsurTech",
            "PropertyInsurance",
            "technology_services",
            "Digital insurance platform",
        ),
        ("AssetManagement", "HedgeFund", "financial_services", "Portfolio management"),
        (
            "PaymentProcessor",
            "EcommercePlatform",
            "technology_services",
            "Payment gateway",
        ),
        (
            "LendingPlatform",
            "SmallBusiness1",
            "startup_funding",
            "Small business loans",
        ),
        (
            "VentureCapital",
            "CryptoCurrency",
            "startup_funding",
            "Blockchain investment",
        ),
    ]

    # Add some smaller companies for fintech lending
    small_businesses = [
        "SmallBusiness1",
        "SmallBusiness2",
        "SmallBusiness3",
        "SmallBusiness4",
    ]
    for business in small_businesses:
        G.add_node(business, sector="services", subsector="small_business")
        all_companies.append(business)

    for debtor, creditor, rel_type, desc in fintech_traditional:
        add_debt_edge(debtor, creditor, rel_type, 1.0, desc)

    # Transportation and Logistics Mega-Hub
    transportation_hub = [
        ("MajorAirline", "AircraftLeasing", "mega_contract", "Aircraft leasing"),
        (
            "AircraftLeasing",
            "AerospaceDefense",
            "supply_chain_tier1",
            "Aircraft manufacturing",
        ),
        ("CargoAirline", "GlobalLogistics", "logistics_services", "Air cargo services"),
        ("ContainerShipping", "PortOperations", "logistics_services", "Port services"),
        ("PortOperations", "GlobalLogistics", "logistics_services", "Port logistics"),
        (
            "FreightForwarder",
            "ContainerShipping",
            "logistics_services",
            "Ocean freight",
        ),
        (
            "LastMileDelivery",
            "EcommercePlatform",
            "logistics_services",
            "Delivery services",
        ),
        (
            "SupplyChainMgmt",
            "FreightForwarder",
            "logistics_services",
            "Supply chain optimization",
        ),
    ]

    for debtor, creditor, rel_type, desc in transportation_hub:
        add_debt_edge(debtor, creditor, rel_type, 1.4, desc)

    # 8. CREATE CROSS-SECTOR INNOVATION NETWORKS

    # Clean Energy and Technology Integration
    clean_tech_network = [
        (
            "SolarEnergy",
            "SemiconductorFab",
            "supply_chain_tier1",
            "Solar panel semiconductors",
        ),
        (
            "WindPower",
            "IndustrialMachinery",
            "supply_chain_tier1",
            "Wind turbine machinery",
        ),
        (
            "ElectricUtility",
            "EnergyTrading",
            "commodity_trading",
            "Renewable energy certificates",
        ),
        (
            "GeothermalEnergy",
            "EngineeringConsult",
            "consulting_services",
            "Geothermal engineering",
        ),
        (
            "HydroElectric",
            "ConstructionMaterials",
            "supply_chain_tier1",
            "Dam construction materials",
        ),
        (
            "EnergyTrading",
            "CryptoCurrency",
            "financial_services",
            "Energy token trading",
        ),
    ]

    for debtor, creditor, rel_type, desc in clean_tech_network:
        add_debt_edge(debtor, creditor, rel_type, 1.1, desc)

    # 9. CREATE ADDITIONAL COMPLEX MULTI-COMPANY CYCLES

    # Pharmaceutical Research and Development Cycle
    pharma_rd_cycle = [
        (
            "PharmaceuticalGiant",
            "ClinicalLabs",
            "consulting_services",
            "Clinical trials",
        ),
        ("ClinicalLabs", "BiotechFirm", "technology_services", "Biotech research"),
        (
            "BiotechFirm",
            "GenericDrugs",
            "licensing_royalty",
            "Drug formulation licensing",
        ),
        (
            "GenericDrugs",
            "ChemicalGiant",
            "supply_chain_tier1",
            "Active pharmaceutical ingredients",
        ),
        (
            "ChemicalGiant",
            "VaccineManufacturer",
            "supply_chain_tier2",
            "Vaccine components",
        ),
        (
            "VaccineManufacturer",
            "HospitalChain",
            "supply_chain_tier1",
            "Vaccine distribution",
        ),
        (
            "HospitalChain",
            "PharmaceuticalGiant",
            "supply_chain_tier1",
            "Pharmaceutical procurement",
        ),
    ]

    for debtor, creditor, rel_type, desc in pharma_rd_cycle:
        add_debt_edge(debtor, creditor, rel_type, 1.3, desc)

    return G


def visualize_network(
    G,
    layout_type="spring",
    figsize=(20, 16),
    node_size_factor=1.0,
    edge_width_factor=1.0,
    show_labels=True,
    show_edge_labels=False,
    filter_sector=None,
    filter_min_debt=None,
    highlight_cycles=False,
    dir_path=os.path.join(PACKAGE_PATH, "figures"),
    title="Business Ecosystem Network",
):
    """
    Visualize the complex business network with multiple options.

    Parameters:
    -----------
    G : nx.DiGraph
        The network graph to visualize
    layout_type : str
        Layout algorithm: 'spring', 'circular', 'kamada_kawai', 'shell', 'hierarchical'
    figsize : tuple
        Figure size (width, height)
    node_size_factor : float
        Multiplier for node sizes
    edge_width_factor : float
        Multiplier for edge widths
    show_labels : bool
        Whether to show node labels
    show_edge_labels : bool
        Whether to show edge labels (debt amounts)
    filter_sector : str or list
        Filter to show only specific sector(s)
    filter_min_debt : float
        Only show edges with debt above this amount
    highlight_cycles : bool
        Whether to highlight cycles in the network
    save_path : str
        Path to save the figure
    title : str
        Title for the plot
    """

    # Create a copy to avoid modifying original
    G_viz = G.copy()

    # Apply filters if specified
    if filter_sector:
        if isinstance(filter_sector, str):
            filter_sector = [filter_sector]
        nodes_to_keep = [
            n for n, d in G_viz.nodes(data=True) if d.get("sector") in filter_sector
        ]
        G_viz = G_viz.subgraph(nodes_to_keep).copy()

    if filter_min_debt:
        edges_to_remove = [
            (u, v)
            for u, v, d in G_viz.edges(data=True)
            if d.get("amount", 0) < filter_min_debt
        ]
        G_viz.remove_edges_from(edges_to_remove)

    # Remove isolated nodes
    G_viz.remove_nodes_from(list(nx.isolates(G_viz)))

    # Set up the figure
    fig, ax = plt.subplots(figsize=figsize)

    # Define color scheme for sectors
    sector_colors = {
        "manufacturing": "#FF6B6B",
        "retail": "#4ECDC4",
        "technology": "#45B7D1",
        "financial": "#96CEB4",
        "energy": "#FFA07A",
        "healthcare": "#98D8C8",
        "telecommunications": "#F7DC6F",
        "transportation": "#BB8FCE",
        "real_estate": "#85C1E2",
        "agriculture": "#82E0AA",
        "materials": "#F8C471",
        "services": "#D7BDE2",
    }

    # Get layout positions
    if layout_type == "spring":
        pos = nx.spring_layout(
            G_viz,
            k=3 / np.sqrt(len(G_viz.nodes())),
            iterations=50,
            weight="amount",
            scale=10,
        )
    elif layout_type == "circular":
        # Group nodes by sector for circular layout
        sectors = defaultdict(list)
        for node, data in G_viz.nodes(data=True):
            sectors[data.get("sector", "unknown")].append(node)
        pos = nx.circular_layout(G_viz)

        # Arrange nodes by sector in circular layout
        angle = 0
        angle_step = 2 * np.pi / len(G_viz.nodes())
        for sector, nodes in sectors.items():
            for i, node in enumerate(nodes):
                angle += angle_step
                pos[node] = (np.cos(angle), np.sin(angle))

    elif layout_type == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G_viz, weight="amount")
    elif layout_type == "shell":
        # Create shells based on node degree
        shells = []
        degrees = dict(G_viz.degree())
        sorted_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)

        # Create 3 shells based on degree
        n_per_shell = len(sorted_nodes) // 3
        shells = [
            [n for n, _ in sorted_nodes[:n_per_shell]],
            [n for n, _ in sorted_nodes[n_per_shell : 2 * n_per_shell]],
            [n for n, _ in sorted_nodes[2 * n_per_shell :]],
        ]
        pos = nx.shell_layout(G_viz, shells)
    elif layout_type == "hierarchical":
        # Use graphviz for hierarchical layout if available
        try:
            pos = nx.nx_agraph.graphviz_layout(G_viz, prog="dot")
        except:
            print("Graphviz not available, using spring layout instead")
            pos = nx.spring_layout(
                G_viz, k=3 / np.sqrt(len(G_viz.nodes())), iterations=50
            )
    else:
        pos = nx.spring_layout(G_viz, k=3 / np.sqrt(len(G_viz.nodes())), iterations=50)

    # Calculate node sizes based on total debt
    node_debts = {}
    for node in G_viz.nodes():
        in_debt = sum(d.get("amount", 0) for _, _, d in G_viz.in_edges(node, data=True))
        out_debt = sum(
            d.get("amount", 0) for _, _, d in G_viz.out_edges(node, data=True)
        )
        node_debts[node] = in_debt + out_debt

    max_debt = max(node_debts.values()) if node_debts else 1
    node_sizes = [
        300 + (node_debts[node] / max_debt) * 2000 * node_size_factor
        for node in G_viz.nodes()
    ]

    # Get node colors
    node_colors = [
        sector_colors.get(G_viz.nodes[node].get("sector", "services"), "#999999")
        for node in G_viz.nodes()
    ]

    # Draw nodes
    nx.draw_networkx_nodes(
        G_viz, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8, ax=ax
    )

    # Draw edges with varying widths based on debt amount
    edge_amounts = [d.get("amount", 0) for _, _, d in G_viz.edges(data=True)]
    max_amount = max(edge_amounts) if edge_amounts else 1
    edge_widths = [
        0.5 + (amount / max_amount) * 5 * edge_width_factor for amount in edge_amounts
    ]

    # Color edges by relationship type
    edge_colors = []
    relationship_colors = {
        "mega_contract": "#FF0000",
        "supply_chain_tier1": "#FF6600",
        "supply_chain_tier2": "#FF9900",
        "financial_services": "#00FF00",
        "technology_services": "#0066FF",
        "consulting_services": "#9900FF",
        "commodity_trading": "#FF00FF",
        "startup_funding": "#00FFFF",
        "other": "#666666",
    }

    for _, _, d in G_viz.edges(data=True):
        rel_type = d.get("relationship", "other")
        edge_colors.append(
            relationship_colors.get(rel_type, relationship_colors["other"])
        )

    # Draw edges
    nx.draw_networkx_edges(
        G_viz,
        pos,
        edge_color=edge_colors,
        width=edge_widths,
        alpha=0.6,
        arrowsize=10,
        arrowstyle="->",
        ax=ax,
    )

    # Highlight cycles if requested
    if highlight_cycles:
        try:
            cycles = list(nx.simple_cycles(G_viz))
            # Highlight only cycles of reasonable length (3-8 nodes)
            cycles = [c for c in cycles if 3 <= len(c) <= 8]

            for i, cycle in enumerate(cycles[:5]):  # Show max 5 cycles
                cycle_edges = [
                    (cycle[j], cycle[(j + 1) % len(cycle)]) for j in range(len(cycle))
                ]
                nx.draw_networkx_edges(
                    G_viz,
                    pos,
                    edgelist=cycle_edges,
                    edge_color="red",
                    width=3,
                    alpha=0.7,
                    ax=ax,
                )
        except:
            print("Could not detect cycles in the filtered graph")

    # Draw labels
    if show_labels:
        labels = {}
        for node in G_viz.nodes():
            # Shorten long names for readability
            label = node
            if len(label) > 15:
                label = label[:12] + "..."
            labels[node] = label

        nx.draw_networkx_labels(
            G_viz, pos, labels, font_size=8, font_weight="bold", ax=ax
        )

    # Draw edge labels (debt amounts) if requested
    if show_edge_labels:
        edge_labels = {}
        for u, v, d in G_viz.edges(data=True):
            amount = d.get("amount", 0)
            edge_labels[(u, v)] = f"${amount / 1000:.0f}K"

        nx.draw_networkx_edge_labels(G_viz, pos, edge_labels, font_size=6, ax=ax)

    # Create legend for sectors
    legend_elements = []
    for sector, color in sector_colors.items():
        if any(G_viz.nodes[n].get("sector") == sector for n in G_viz.nodes()):
            legend_elements.append(
                plt.Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor=color,
                    markersize=10,
                    label=sector.replace("_", " ").title(),
                )
            )

    ax.legend(
        handles=legend_elements,
        loc="upper left",
        bbox_to_anchor=(1.02, 1),
        title="Sectors",
        fontsize=10,
    )

    # Add title and stats
    plt.title(
        f"{title}\nNodes: {G_viz.number_of_nodes()}, Edges: {G_viz.number_of_edges()}",
        fontsize=16,
        pad=20,
    )

    # Remove axes
    ax.set_axis_off()

    # Adjust layout
    plt.tight_layout()

    # Save if path provided
    if dir_path:
        plt.savefig(os.path.join(dir_path, title), dpi=300, bbox_inches="tight")

    # Print network statistics
    print_network_stats(G_viz)


def print_network_stats(G):
    """Print detailed statistics about the network"""
    print("\n=== Network Statistics ===")
    print(f"Total nodes: {G.number_of_nodes()}")
    print(f"Total edges: {G.number_of_edges()}")
    print(f"Network density: {nx.density(G):.4f}")

    # Degree statistics
    degrees = dict(G.degree())
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())

    print(f"\nAverage degree: {np.mean(list(degrees.values())):.2f}")
    print(f"Max degree: {max(degrees.values())}")
    print(f"Node with max degree: {max(degrees, key=degrees.get)}")

    # Debt statistics
    total_debt = sum(d.get("amount", 0) for _, _, d in G.edges(data=True))
    avg_debt = total_debt / G.number_of_edges() if G.number_of_edges() > 0 else 0

    print(f"\nTotal debt in network: ${total_debt:,.0f}")
    print(f"Average debt per edge: ${avg_debt:,.0f}")

    # Find most indebted companies
    company_debts = defaultdict(float)
    for u, v, d in G.edges(data=True):
        company_debts[u] += d.get("amount", 0)

    top_debtors = sorted(company_debts.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nTop 5 debtor companies:")
    for company, debt in top_debtors:
        print(f"  {company}: ${debt:,.0f}")

    # Sector statistics
    sector_counts = defaultdict(int)
    for _, data in G.nodes(data=True):
        sector_counts[data.get("sector", "unknown")] += 1

    print("\nNodes per sector:")
    for sector, count in sorted(sector_counts.items()):
        print(f"  {sector}: {count}")

    # Connectivity
    if nx.is_weakly_connected(G):
        print("\nNetwork is weakly connected")
    else:
        print(
            f"\nNetwork has {nx.number_weakly_connected_components(G)} weakly connected components"
        )

    # Detect important cycles
    try:
        cycles = list(nx.simple_cycles(G))
        cycle_lengths = [len(c) for c in cycles]
        if cycle_lengths:
            print(f"\nTotal cycles found: {len(cycles)}")
            print(f"Cycle length range: {min(cycle_lengths)} - {max(cycle_lengths)}")
            print(f"Average cycle length: {np.mean(cycle_lengths):.2f}")
    except:
        print("\nCycle detection skipped (too complex)")


def visualize_sector_comparison(
    G,
    sectors_to_compare=None,
    figsize=(16, 10),
    dir_path=os.path.join(PACKAGE_PATH, "figures"),
):
    """
    Create a comparison visualization of different sectors
    """
    if sectors_to_compare is None:
        # Get all unique sectors
        all_sectors = set(
            data.get("sector", "unknown") for _, data in G.nodes(data=True)
        )
        sectors_to_compare = list(all_sectors)[:6]  # Compare up to 6 sectors

    n_sectors = len(sectors_to_compare)
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    axes = axes.flatten()

    for i, sector in enumerate(sectors_to_compare):
        if i >= len(axes):
            break

        ax = axes[i]

        # Create subgraph for this sector
        sector_nodes = [n for n, d in G.nodes(data=True) if d.get("sector") == sector]

        # Include nodes connected to sector nodes
        connected_nodes = set(sector_nodes)
        for node in sector_nodes:
            connected_nodes.update(G.predecessors(node))
            connected_nodes.update(G.successors(node))

        subgraph = G.subgraph(connected_nodes).copy()

        # Remove isolated nodes
        subgraph.remove_nodes_from(list(nx.isolates(subgraph)))

        if subgraph.number_of_nodes() == 0:
            ax.text(
                0.5,
                0.5,
                f"No connections for {sector}",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )
            ax.set_title(f"{sector.title()} Network")
            ax.axis("off")
            continue

        # Layout
        pos = nx.spring_layout(subgraph, k=1, iterations=50)

        # Node colors (highlight sector nodes)
        node_colors = [
            "red" if n in sector_nodes else "lightblue" for n in subgraph.nodes()
        ]

        # Draw
        nx.draw(
            subgraph,
            pos,
            ax=ax,
            node_color=node_colors,
            with_labels=True,
            font_size=6,
            node_size=300,
            edge_color="gray",
            alpha=0.7,
            arrows=True,
        )

        ax.set_title(
            f"{sector.title()} Network\n"
            f"({len(sector_nodes)} core nodes, "
            f"{subgraph.number_of_edges()} edges)"
        )

    # Remove empty subplots
    for i in range(n_sectors, len(axes)):
        fig.delaxes(axes[i])

    plt.suptitle("Sector-wise Network Analysis", fontsize=16)
    plt.tight_layout()
    plt.savefig(
        os.path.join(dir_path, "Sector Comparison"), dpi=300, bbox_inches="tight"
    )
    print(f"Figure saved to {os.path.join(dir_path, 'Sector Comparison')}")


def visualize_supply_chain_tiers(
    G,
    root_company=None,
    max_tiers=4,
    figsize=(20, 12),
    dir_path=os.path.join(PACKAGE_PATH, "figures"),
):
    """
    Visualize supply chain tiers starting from a root company
    """
    if root_company is None:
        # Find a company with many connections
        degrees = dict(G.degree())
        root_company = max(degrees, key=degrees.get)

    # Find all companies in supply chain tiers
    tiers = {0: {root_company}}
    visited = {root_company}

    for tier in range(1, max_tiers + 1):
        current_tier = set()
        for company in tiers[tier - 1]:
            # Add suppliers (predecessors)
            for supplier in G.predecessors(company):
                if supplier not in visited:
                    edge_data = G.get_edge_data(company, supplier)
                    if edge_data and "supply_chain" in edge_data.get(
                        "relationship", ""
                    ):
                        current_tier.add(supplier)
                        visited.add(supplier)

            # Add customers (successors)
            for customer in G.successors(company):
                if customer not in visited:
                    edge_data = G.get_edge_data(customer, company)
                    if edge_data and "supply_chain" in edge_data.get(
                        "relationship", ""
                    ):
                        current_tier.add(customer)
                        visited.add(customer)

        if current_tier:
            tiers[tier] = current_tier
        else:
            break

    # Create subgraph with only these nodes
    all_tier_nodes = set()
    for tier_nodes in tiers.values():
        all_tier_nodes.update(tier_nodes)

    subgraph = G.subgraph(all_tier_nodes).copy()

    # Create hierarchical layout
    pos = {}
    tier_width = 2.0
    tier_height = 2.0

    for tier, nodes in tiers.items():
        n_nodes = len(nodes)
        if n_nodes == 0:
            continue

        # Arrange nodes horizontally at each tier
        x_positions = np.linspace(
            -tier_width * n_nodes / 4, tier_width * n_nodes / 4, n_nodes
        )
        y_position = -tier * tier_height

        for i, node in enumerate(sorted(nodes)):
            pos[node] = (x_positions[i], y_position)

    # Visualization
    fig, ax = plt.subplots(figsize=figsize)

    # Color nodes by tier
    colors = plt.cm.viridis(np.linspace(0, 1, len(tiers)))

    for tier, nodes in tiers.items():
        nx.draw_networkx_nodes(
            subgraph,
            pos,
            nodelist=list(nodes),
            node_color=[colors[tier]],
            node_size=500,
            label=f"Tier {tier}",
            ax=ax,
        )

    # Draw edges
    nx.draw_networkx_edges(
        subgraph, pos, edge_color="gray", alpha=0.5, arrows=True, ax=ax
    )

    # Labels
    nx.draw_networkx_labels(subgraph, pos, font_size=8, ax=ax)

    plt.title(f"Supply Chain Tiers from {root_company}", fontsize=16)
    plt.legend(loc="best")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(
        os.path.join(dir_path, "Supply Chain Tiers from {root_company}"),
        dpi=300,
        bbox_inches="tight",
    )
    print(
        f"Figure saved to {os.path.join(dir_path, 'Supply Chain Tiers from {root_company}')}"
    )

    # Print tier statistics
    print(f"\nSupply Chain Analysis from {root_company}:")
    for tier, nodes in tiers.items():
        print(f"Tier {tier}: {len(nodes)} companies")
        if tier > 0:
            print(
                f"  Companies: {', '.join(sorted(nodes)[:5])}"
                f"{'...' if len(nodes) > 5 else ''}"
            )


# Example usage function
def demo_visualizations(G, dir_path=os.path.join(PACKAGE_PATH, "figures")):
    """
    Demonstrate various visualization options
    """
    print("Creating network visualizations...")

    # 1. Full network with spring layout
    print("\n1. Full network visualization")
    visualize_network(
        G,
        layout_type="spring",
        title="Complete Business Ecosystem Network",
        dir_path=dir_path,
    )

    # 2. Technology sector focus
    print("\n2. Technology sector network")
    visualize_network(
        G,
        filter_sector="technology",
        layout_type="kamada_kawai",
        title="Technology Sector Network",
        dir_path=dir_path,
    )

    # 3. High-value relationships only
    print("\n3. High-value debt relationships over $500K")
    visualize_network(
        G,
        filter_min_debt=500000,
        show_edge_labels=True,
        title="High-Value Debt Network over $500K",
        dir_path=dir_path,
    )

    # 4. Sector comparison
    print("\n4. Sector comparison")
    visualize_sector_comparison(
        G,
        sectors_to_compare=["technology", "financial", "manufacturing", "healthcare"],
        dir_path=dir_path,
    )

    # 5. Supply chain visualization
    print("\n5. Supply chain tiers")
    visualize_supply_chain_tiers(G, root_company="AutoManufacturing", dir_path=dir_path)


def export_to_gexf(
    G=None, output_dir=os.path.join(PACKAGE_PATH, "exports"), file_name=None
):
    gexf_path = os.path.join(output_dir, f"{file_name}.gexf")
    nx.write_gexf(G, gexf_path)
    print(f"✓ Exported to GEXF: {gexf_path}")


def export_to_graphml(
    G=None, output_dir=os.path.join(PACKAGE_PATH, "exports"), file_name=None
):
    # 2. Export to GraphML
    graphml_path = os.path.join(output_dir, f"{file_name}.graphml")
    nx.write_graphml(G, graphml_path)
    print(f"✓ Exported to GraphML: {graphml_path}")


if __name__ == "__main__":
    G = create_complex_network()

    # Export to gexf (Gephi compatible)
    export_to_gexf(G, file_name="full_network")

    # Visualize the network with matplotlib
    visualize_network(G)
