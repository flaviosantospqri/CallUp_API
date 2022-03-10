from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from app.models.category_model import Category
from app.models.subcategory_model import SubCategory
from app.models.sector_model import Sector
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(getenv("DB_URI"))
Session = sessionmaker(bind=engine)
session: Session = Session()


def gener_data_sector():

    governing = {"name": "Governing"}
    financial = {"name": "Financial"}
    commercial = {"name": "Commercial"}
    human_resources = {"name": "Human_resources"}
    operational = {"name": "Operational"}

    data = [governing, financial, commercial, human_resources, operational]

    for element in data:
        value_element = Sector(**element)
        session.add(value_element)
        session.commit()


def gener_data_categories():

    system_analysis = {"name": "System Analysis"}
    networks = {"name": "Networks"}
    development = {"name": "Development"}
    hardware = {"name": "Hardware"}
    peripherals = {"name": "Peripherals"}
    support = {"name": "Support"}
    governance_system = {"name": "Governance System"}

    data = [
        system_analysis,
        networks,
        development,
        hardware,
        peripherals,
        support,
        governance_system,
    ]

    for element in data:
        value_element = Category(**element)
        session.add(value_element)
        session.commit()


def gener_data_subcategories():
    try:
        system_analysis = (
            session.query(Category).filter_by(name="System Analysis").first()
        )
        print(system_analysis)
        performance_analysis = {
            "category_id": system_analysis.id,
            "name": "Performance Analysis",
        }
        feature_analysis = {
            "category_id": system_analysis.id,
            "name": "Feature Analysis",
        }
        error_analysis = {"category_id": system_analysis.id, "name": "Error Analysis"}
        print(performance_analysis)
        networks = session.query(Category).filter_by(name="Networks").first()
        connection_failures = {
            "category_id": networks.id,
            "name": "Connection Failures",
        }
        assemble_internal_network = {
            "category_id": networks.id,
            "name": "Assemble Internal Network",
        }
        assemble_external_network = {
            "category_id": networks.id,
            "name": "Assemble External Network",
        }
        review_network = {"category_id": networks.id, "name": "Review Network"}
        review_packet_loss = {"category_id": networks.id, "name": " Review Packet Loss"}

        development = session.query(Category).filter_by(name="Development").first()
        development_site = {"category_id": development.id, "name": "Development Site"}
        development_software = {
            "category_id": development.id,
            "name": "Development Software",
        }
        development_plann = {"category_id": development.id, "name": "Development Plann"}
        development_digital_marketing = {
            "category_id": development.id,
            "name": "Development Digital Marketing",
        }

        hardware = session.query(Category).filter_by(name="Hardware").first()
        mounting = {"category_id": hardware.id, "name": "Mounting"}
        maintenance = {"category_id": hardware.id, "name": "Maintenance"}
        repair = {"category_id": hardware.id, "name": "Repair"}
        acquisition = {"category_id": hardware.id, "name": "Acquisition"}

        peripherals = session.query(Category).filter_by(name="Peripherals").first()
        keyboard = {"category_id": peripherals.id, "name": "Keyboard"}
        mouse = {"category_id": peripherals.id, "name": "Mouse"}
        monitor = {"category_id": peripherals.id, "name": "Monitor"}
        barcode_reader = {"category_id": peripherals.id, "name": "Barcode Reader"}
        sound_box = {"category_id": peripherals.id, "name": "Sound Box"}
        others = {"category_id": peripherals.id, "name": "Others"}

        support = session.query(Category).filter_by(name="Support").first()
        call = {"category_id": support.id, "name": "Call"}
        chat = {"category_id": support.id, "name": "Chat"}

        governance_system = (
            session.query(Category).filter_by(name="Governance System").first()
        )

        network_data_management = {
            "category_id": governance_system.id,
            "name": "Network data management",
        }

        safe_browsing = {"category_id": governance_system.id, "name": "Safe browsing"}
        evaluation_of_services_performed = {
            "category_id": governance_system.id,
            "name": "Evaluation of services performed",
        }

        data = [
            performance_analysis,
            feature_analysis,
            error_analysis,
            connection_failures,
            assemble_internal_network,
            assemble_external_network,
            review_network,
            review_packet_loss,
            development_site,
            development_software,
            development_plann,
            development_digital_marketing,
            mounting,
            maintenance,
            repair,
            acquisition,
            keyboard,
            mouse,
            monitor,
            barcode_reader,
            sound_box,
            others,
            call,
            chat,
            network_data_management,
            safe_browsing,
            evaluation_of_services_performed,
        ]

        for element in data:
            value_element = SubCategory(**element)
            session.add(value_element)
            session.commit()
    except:
        {"message": "categories not exists"}


gener_data_sector()
gener_data_categories()
gener_data_subcategories()

session.close()
