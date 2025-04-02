--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: ai_worker_skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_worker_skills (
    ai_worker_id uuid NOT NULL,
    skill_id uuid NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.ai_worker_skills OWNER TO postgres;

--
-- Name: ai_worker_socials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_worker_socials (
    ai_worker_id uuid NOT NULL,
    social_id uuid NOT NULL,
    org_id uuid,
    user_id uuid,
    page_access_token text NOT NULL,
    app_id character varying(255) NOT NULL,
    page_id character varying(255) NOT NULL,
    app_secret_key text NOT NULL,
    is_verified boolean,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    page_refresh_token text
);


ALTER TABLE public.ai_worker_socials OWNER TO postgres;

--
-- Name: ai_worker_statistics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_worker_statistics (
    ai_worker_id uuid NOT NULL,
    total_orders_closed integer NOT NULL,
    conversation_ratings json NOT NULL,
    avg_rating double precision NOT NULL,
    total_tokens_used integer NOT NULL,
    total_conversation integer NOT NULL,
    successful_conversations integer NOT NULL,
    failed_conversations integer NOT NULL,
    avg_response_time double precision NOT NULL,
    last_active timestamp with time zone NOT NULL,
    errors_logged integer NOT NULL,
    total_sales_value integer NOT NULL,
    peak_usage_time text NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.ai_worker_statistics OWNER TO postgres;

--
-- Name: ai_workers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ai_workers (
    status character varying(50) NOT NULL,
    ai_agent_name character varying(100) NOT NULL,
    description text NOT NULL,
    model character varying(100) NOT NULL,
    temperature double precision NOT NULL,
    max_token integer NOT NULL,
    auto_confirm_order boolean NOT NULL,
    total_message integer NOT NULL,
    total_token integer NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    store_id uuid NOT NULL
);


ALTER TABLE public.ai_workers OWNER TO postgres;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: audits; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audits (
    user_id uuid,
    org_id uuid,
    action character varying(50) NOT NULL,
    table_name character varying(255) NOT NULL,
    record_id uuid NOT NULL,
    details text,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.audits OWNER TO postgres;

--
-- Name: bank_accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bank_accounts (
    store_id uuid NOT NULL,
    bank_account_holder character varying(255) NOT NULL,
    bank_account_number character varying(255) NOT NULL,
    bank_name character varying(255) NOT NULL,
    is_used boolean NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.bank_accounts OWNER TO postgres;

--
-- Name: brands; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.brands (
    name character varying(255) NOT NULL,
    ascii_name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description text,
    image_link character varying(2083),
    category_id uuid,
    subcategory_id uuid,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    org_id uuid
);


ALTER TABLE public.brands OWNER TO postgres;

--
-- Name: buyer_infos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.buyer_infos (
    product_type_id uuid NOT NULL,
    buyer_full_name character varying(255) NOT NULL,
    buyer_phone_number character varying(15) NOT NULL,
    note text,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    store_id uuid NOT NULL,
    buyer_id character varying NOT NULL
);


ALTER TABLE public.buyer_infos OWNER TO postgres;

--
-- Name: cancel_reasons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cancel_reasons (
    reason character varying(255),
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.cancel_reasons OWNER TO postgres;

--
-- Name: cart_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart_items (
    cart_id uuid NOT NULL,
    product_detail_id uuid,
    product_id uuid,
    object_type character varying(15) NOT NULL,
    warehouse_code character varying(15),
    sku_code character varying NOT NULL,
    type character varying(30) NOT NULL,
    quantity integer NOT NULL,
    display_price double precision NOT NULL,
    discounted_price double precision NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.cart_items OWNER TO postgres;

--
-- Name: carts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.carts (
    user_id uuid,
    store_id uuid,
    social_cus_id character varying(255) NOT NULL,
    product_type_id uuid NOT NULL,
    total_item integer NOT NULL,
    total_display_price double precision NOT NULL,
    total_discounted_price double precision NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.carts OWNER TO postgres;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    product_type_id uuid NOT NULL,
    name text NOT NULL,
    "position" integer NOT NULL,
    slug text NOT NULL,
    description text NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: communications_banners; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.communications_banners (
    title character varying(255) NOT NULL,
    content text NOT NULL,
    image_url character varying(2083) NOT NULL,
    link_url character varying(2083) NOT NULL,
    display_position integer NOT NULL,
    start_date timestamp with time zone NOT NULL,
    end_date timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.communications_banners OWNER TO postgres;

--
-- Name: conversations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.conversations (
    ai_worker_id uuid NOT NULL,
    user_id uuid NOT NULL,
    org_id uuid,
    conversation_name character varying(100) NOT NULL,
    rating_score integer,
    is_taken boolean NOT NULL,
    ended_at timestamp with time zone,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.conversations OWNER TO postgres;

--
-- Name: departments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departments (
    org_id uuid,
    name character varying(255) NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.departments OWNER TO postgres;

--
-- Name: districts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.districts (
    province_code integer NOT NULL,
    district_code integer NOT NULL,
    district_name character varying(255) NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.districts OWNER TO postgres;

--
-- Name: keywords; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.keywords (
    keyword_name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.keywords OWNER TO postgres;

--
-- Name: knowledge_bases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.knowledge_bases (
    ai_worker_id uuid NOT NULL,
    title character varying(255) NOT NULL,
    aws_file_url character varying(255) NOT NULL,
    aws_file_name character varying(255) NOT NULL,
    content_type character varying(255) NOT NULL,
    file_size double precision NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.knowledge_bases OWNER TO postgres;

--
-- Name: medias; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.medias (
    product_id uuid NOT NULL,
    media_type character varying(255) NOT NULL,
    media_link text NOT NULL,
    "position" integer NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.medias OWNER TO postgres;

--
-- Name: membership_packages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.membership_packages (
    package_title character varying(255) NOT NULL,
    price double precision NOT NULL,
    available_model character varying(255) NOT NULL,
    message_credits integer NOT NULL,
    number_of_chatbots integer NOT NULL,
    max_character_per_chatbot integer NOT NULL,
    live_agent_takeover boolean NOT NULL,
    remove_label boolean NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.membership_packages OWNER TO postgres;

--
-- Name: messages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.messages (
    conversation_id uuid NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    store_id uuid,
    question text NOT NULL,
    answer text NOT NULL
);


ALTER TABLE public.messages OWNER TO postgres;

--
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notifications (
    org_id uuid,
    user_id uuid,
    title character varying(255) NOT NULL,
    content text NOT NULL,
    type character varying(50) NOT NULL,
    is_read boolean NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- Name: option_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.option_groups (
    name character varying(255) NOT NULL,
    description text,
    max_quantity integer,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.option_groups OWNER TO postgres;

--
-- Name: options; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.options (
    option_group_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    ascii_name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    unit_price double precision NOT NULL,
    image_link text NOT NULL,
    description text NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.options OWNER TO postgres;

--
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    order_id uuid NOT NULL,
    product_detail_id uuid NOT NULL,
    product_id uuid NOT NULL,
    object_type character varying(255) NOT NULL,
    quantity integer NOT NULL,
    price double precision NOT NULL,
    promotion_price double precision NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    product_detail_image_link character varying(255) NOT NULL
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- Name: order_payment_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_payment_items (
    order_id uuid NOT NULL,
    code character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    amount double precision NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.order_payment_items OWNER TO postgres;

--
-- Name: order_shipping_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_shipping_details (
    order_id uuid NOT NULL,
    step_id uuid,
    auto_next_workflow_step_id uuid,
    shipping_method_id uuid NOT NULL,
    workflow_id uuid,
    provisional_amount double precision NOT NULL,
    shipping_amount double precision NOT NULL,
    customer_address text NOT NULL,
    customer_email character varying(255),
    customer_address_type character varying(255) NOT NULL,
    auto_next_workflow_step_at timestamp with time zone,
    auto_error text,
    is_allow_auto boolean,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.order_shipping_details OWNER TO postgres;

--
-- Name: order_states; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_states (
    code character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.order_states OWNER TO postgres;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    payment_method_id uuid NOT NULL,
    cancel_reason_id uuid,
    buyer_info_id uuid NOT NULL,
    code character varying(255) NOT NULL,
    state character varying(255) NOT NULL,
    amount double precision NOT NULL,
    customer_name character varying(255) NOT NULL,
    customer_phone character varying(255) NOT NULL,
    product_type_id uuid NOT NULL,
    user_id uuid,
    store_id uuid NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    org_id uuid
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: organization_memberships; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organization_memberships (
    org_id uuid NOT NULL,
    package_id uuid NOT NULL,
    expire_at timestamp with time zone,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.organization_memberships OWNER TO postgres;

--
-- Name: organizations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organizations (
    owner_id uuid NOT NULL,
    org_logo text NOT NULL,
    org_name character varying(255) NOT NULL,
    org_email character varying(255) NOT NULL,
    org_type character varying(255) NOT NULL,
    org_address text NOT NULL,
    representative_name character varying(255) NOT NULL,
    representative_phone character varying(255),
    representative_address text,
    description text,
    is_open boolean NOT NULL,
    is_terms_accepted boolean NOT NULL,
    terms_accepted_at timestamp with time zone,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.organizations OWNER TO postgres;

--
-- Name: payment_methods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment_methods (
    name character varying(255) NOT NULL,
    type character varying(255) NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.payment_methods OWNER TO postgres;

--
-- Name: permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permissions (
    name character varying(255) NOT NULL,
    description text NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.permissions OWNER TO postgres;

--
-- Name: product_details; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_details (
    product_id uuid NOT NULL,
    store_id uuid NOT NULL,
    is_published boolean,
    sku_code character varying(255) NOT NULL,
    total_sold integer NOT NULL,
    product_detail_name character varying(255) NOT NULL,
    quantity_promotion_sold integer NOT NULL,
    image_link text NOT NULL,
    price double precision NOT NULL,
    b2b_price double precision,
    promotion_price double precision,
    available_quantity integer NOT NULL,
    has_expiry_date boolean NOT NULL,
    attribute json,
    category_id uuid,
    product_type_id uuid,
    keyword_id uuid,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    subcategory_id uuid
);


ALTER TABLE public.product_details OWNER TO postgres;

--
-- Name: product_keywords; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_keywords (
    product_id uuid NOT NULL,
    keyword_id uuid NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.product_keywords OWNER TO postgres;

--
-- Name: product_promotions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_promotions (
    product_id uuid NOT NULL,
    promotion_id uuid NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.product_promotions OWNER TO postgres;

--
-- Name: product_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_types (
    name character varying(255) NOT NULL,
    ascii_name character varying(255) NOT NULL,
    "position" integer NOT NULL,
    slug character varying(255) NOT NULL,
    description text NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.product_types OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    subcategory_id uuid NOT NULL,
    brand_id uuid,
    is_published boolean NOT NULL,
    name character varying(255) NOT NULL,
    ascii_name character varying(255) NOT NULL,
    type character varying(255) NOT NULL,
    image_link text NOT NULL,
    description text NOT NULL,
    html_content text,
    total_rating integer,
    avg_rating double precision,
    total_sold integer NOT NULL,
    is_freeship boolean NOT NULL,
    flashsale_startdate timestamp with time zone,
    flashsale_enddate timestamp with time zone,
    percent_discount double precision,
    is_flashsale boolean,
    length double precision,
    width double precision,
    height double precision,
    package_weight double precision,
    category_id uuid,
    product_type_id uuid,
    keyword_id uuid,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    org_id uuid,
    video_link text
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: promotions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.promotions (
    store_id uuid NOT NULL,
    promotion_name character varying(255) NOT NULL,
    start_date timestamp with time zone,
    end_date timestamp with time zone,
    discount_percent integer NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.promotions OWNER TO postgres;

--
-- Name: provinces; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.provinces (
    province_name character varying(255) NOT NULL,
    province_code integer NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.provinces OWNER TO postgres;

--
-- Name: receivers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.receivers (
    buyer_info_id uuid NOT NULL,
    receiver_full_name character varying(255) NOT NULL,
    receiver_phone_number character varying(255) NOT NULL,
    note text,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.receivers OWNER TO postgres;

--
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    customer_id uuid,
    org_id uuid,
    entity_type character varying(255) NOT NULL,
    rating integer NOT NULL,
    review_comment text NOT NULL,
    heart_count integer,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_permissions (
    role_id uuid NOT NULL,
    permission_id uuid NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.role_permissions OWNER TO postgres;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    name character varying(255) NOT NULL,
    description text NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- Name: setting_products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.setting_products (
    option_id uuid NOT NULL,
    product_id uuid NOT NULL,
    max_quantity integer NOT NULL,
    total_price double precision NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.setting_products OWNER TO postgres;

--
-- Name: shipping_infos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shipping_infos (
    receiver_id uuid NOT NULL,
    address text,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    province_code integer NOT NULL,
    district_code integer NOT NULL,
    ward_code integer NOT NULL
);


ALTER TABLE public.shipping_infos OWNER TO postgres;

--
-- Name: shipping_methods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shipping_methods (
    shipping_provider_id uuid,
    name character varying(255) NOT NULL,
    price double precision NOT NULL,
    estimate_day integer NOT NULL,
    shipping_plan text NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.shipping_methods OWNER TO postgres;

--
-- Name: shipping_providers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shipping_providers (
    name character varying(255) NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.shipping_providers OWNER TO postgres;

--
-- Name: skills; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.skills (
    name character varying(255) NOT NULL,
    description text NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.skills OWNER TO postgres;

--
-- Name: socials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.socials (
    platform character varying(255) NOT NULL,
    icon_url text,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.socials OWNER TO postgres;

--
-- Name: step_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.step_logs (
    order_shipping_detail_id uuid NOT NULL,
    step_id uuid NOT NULL,
    delivery_order_id uuid,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.step_logs OWNER TO postgres;

--
-- Name: store_locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_locations (
    province_id uuid,
    district_id uuid,
    ward_id uuid,
    longitude character varying(255) NOT NULL,
    latitude character varying(255) NOT NULL,
    detailed_address text NOT NULL,
    province_code character varying(255) NOT NULL,
    district_code character varying(255) NOT NULL,
    ward_code character varying(255) NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.store_locations OWNER TO postgres;

--
-- Name: store_payment_histories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_payment_histories (
    store_id uuid NOT NULL,
    org_id uuid NOT NULL,
    bank_account_id uuid NOT NULL,
    payment_date timestamp with time zone NOT NULL,
    payment_amount double precision NOT NULL,
    payment_method character varying(255) NOT NULL,
    transaction_reference character varying(255) NOT NULL,
    notes text,
    is_successful boolean NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.store_payment_histories OWNER TO postgres;

--
-- Name: store_shipping_providers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_shipping_providers (
    store_id uuid NOT NULL,
    shipping_provider_id uuid NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.store_shipping_providers OWNER TO postgres;

--
-- Name: stores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stores (
    org_id uuid NOT NULL,
    owner_id uuid NOT NULL,
    store_location_id uuid,
    is_open boolean NOT NULL,
    warehouse_code character varying(255) NOT NULL,
    org_name character varying(255) NOT NULL,
    store_name character varying(255) NOT NULL,
    contact_info_name character varying(255) NOT NULL,
    contact_info_phone character varying(255) NOT NULL,
    fan_page text NOT NULL,
    zalo_oa text NOT NULL,
    website text NOT NULL,
    invoice_issue boolean NOT NULL,
    is_cod boolean NOT NULL,
    is_prepayment boolean NOT NULL,
    max_sku_purchased integer NOT NULL,
    min_cart_value double precision NOT NULL,
    max_order_value double precision NOT NULL,
    is_auto_confirm boolean NOT NULL,
    waiting_time integer,
    is_send_notification boolean NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    contact_info_sender_psid character varying(255)
);


ALTER TABLE public.stores OWNER TO postgres;

--
-- Name: subcategories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subcategories (
    category_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    "position" integer NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.subcategories OWNER TO postgres;

--
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_sessions (
    user_id uuid NOT NULL,
    refresh_token text NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.user_sessions OWNER TO postgres;

--
-- Name: user_stores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_stores (
    user_id uuid NOT NULL,
    store_id uuid NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    store_name character varying,
    user_name character varying,
    org_id uuid
);


ALTER TABLE public.user_stores OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    role_id uuid NOT NULL,
    org_id uuid,
    display_name character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    phone_number character varying(255),
    avatar_url text,
    avatar_fallback text,
    is_verified boolean NOT NULL,
    is_change_password boolean NOT NULL,
    verification_code character varying(255),
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone,
    department_id uuid
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: wards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wards (
    province_code integer NOT NULL,
    district_code integer NOT NULL,
    ward_code integer NOT NULL,
    ward_name character varying(255) NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.wards OWNER TO postgres;

--
-- Name: workflow_steps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflow_steps (
    order_workflow_id uuid NOT NULL,
    order_state_id uuid NOT NULL,
    start_point text,
    allow_payment boolean NOT NULL,
    allow_review boolean NOT NULL,
    allow_user_cancel boolean NOT NULL,
    allow_repurchase boolean NOT NULL,
    allow_make_delivery boolean NOT NULL,
    is_user_cancel boolean NOT NULL,
    is_system_cancel boolean NOT NULL,
    is_on_delivery boolean NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.workflow_steps OWNER TO postgres;

--
-- Name: workflows; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workflows (
    name character varying(255) NOT NULL,
    id uuid NOT NULL,
    is_active boolean,
    created_at timestamp with time zone,
    updated_at timestamp with time zone,
    deleted_at timestamp with time zone
);


ALTER TABLE public.workflows OWNER TO postgres;

--
-- Name: ai_worker_skills ai_worker_skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_worker_skills
    ADD CONSTRAINT ai_worker_skills_pkey PRIMARY KEY (id);


--
-- Name: ai_worker_socials ai_worker_socials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_worker_socials
    ADD CONSTRAINT ai_worker_socials_pkey PRIMARY KEY (id);


--
-- Name: ai_worker_statistics ai_worker_statistics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_worker_statistics
    ADD CONSTRAINT ai_worker_statistics_pkey PRIMARY KEY (id);


--
-- Name: ai_workers ai_workers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_workers
    ADD CONSTRAINT ai_workers_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: audits audits_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audits
    ADD CONSTRAINT audits_pkey PRIMARY KEY (id);


--
-- Name: bank_accounts bank_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank_accounts
    ADD CONSTRAINT bank_accounts_pkey PRIMARY KEY (id);


--
-- Name: brands brands_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_pkey PRIMARY KEY (id);


--
-- Name: buyer_infos buyer_infos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.buyer_infos
    ADD CONSTRAINT buyer_infos_pkey PRIMARY KEY (id);


--
-- Name: cancel_reasons cancel_reasons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cancel_reasons
    ADD CONSTRAINT cancel_reasons_pkey PRIMARY KEY (id);


--
-- Name: cart_items cart_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);


--
-- Name: cart_items cart_items_sku_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_sku_code_key UNIQUE (sku_code);


--
-- Name: carts carts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: communications_banners communications_banners_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.communications_banners
    ADD CONSTRAINT communications_banners_pkey PRIMARY KEY (id);


--
-- Name: conversations conversations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_pkey PRIMARY KEY (id);


--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (id);


--
-- Name: districts districts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.districts
    ADD CONSTRAINT districts_pkey PRIMARY KEY (id);


--
-- Name: keywords keywords_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keywords
    ADD CONSTRAINT keywords_pkey PRIMARY KEY (id);


--
-- Name: knowledge_bases knowledge_bases_aws_file_url_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.knowledge_bases
    ADD CONSTRAINT knowledge_bases_aws_file_url_key UNIQUE (aws_file_url);


--
-- Name: knowledge_bases knowledge_bases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.knowledge_bases
    ADD CONSTRAINT knowledge_bases_pkey PRIMARY KEY (id);


--
-- Name: medias medias_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medias
    ADD CONSTRAINT medias_pkey PRIMARY KEY (id);


--
-- Name: membership_packages membership_packages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.membership_packages
    ADD CONSTRAINT membership_packages_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: option_groups option_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.option_groups
    ADD CONSTRAINT option_groups_pkey PRIMARY KEY (id);


--
-- Name: options options_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_pkey PRIMARY KEY (id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- Name: order_payment_items order_payment_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_payment_items
    ADD CONSTRAINT order_payment_items_pkey PRIMARY KEY (id);


--
-- Name: order_shipping_details order_shipping_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_shipping_details
    ADD CONSTRAINT order_shipping_details_pkey PRIMARY KEY (id);


--
-- Name: order_states order_states_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_states
    ADD CONSTRAINT order_states_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: organization_memberships organization_memberships_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_memberships
    ADD CONSTRAINT organization_memberships_pkey PRIMARY KEY (id);


--
-- Name: organizations organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (id);


--
-- Name: payment_methods payment_methods_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: product_details product_details_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_details
    ADD CONSTRAINT product_details_pkey PRIMARY KEY (id);


--
-- Name: product_keywords product_keywords_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_keywords
    ADD CONSTRAINT product_keywords_pkey PRIMARY KEY (id);


--
-- Name: product_promotions product_promotions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_promotions
    ADD CONSTRAINT product_promotions_pkey PRIMARY KEY (id);


--
-- Name: product_types product_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_types
    ADD CONSTRAINT product_types_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: promotions promotions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotions
    ADD CONSTRAINT promotions_pkey PRIMARY KEY (id);


--
-- Name: provinces provinces_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.provinces
    ADD CONSTRAINT provinces_pkey PRIMARY KEY (id);


--
-- Name: receivers receivers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.receivers
    ADD CONSTRAINT receivers_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: setting_products setting_products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.setting_products
    ADD CONSTRAINT setting_products_pkey PRIMARY KEY (id);


--
-- Name: shipping_infos shipping_infos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipping_infos
    ADD CONSTRAINT shipping_infos_pkey PRIMARY KEY (id);


--
-- Name: shipping_methods shipping_methods_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipping_methods
    ADD CONSTRAINT shipping_methods_pkey PRIMARY KEY (id);


--
-- Name: shipping_providers shipping_providers_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipping_providers
    ADD CONSTRAINT shipping_providers_name_key UNIQUE (name);


--
-- Name: shipping_providers shipping_providers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipping_providers
    ADD CONSTRAINT shipping_providers_pkey PRIMARY KEY (id);


--
-- Name: skills skills_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (id);


--
-- Name: socials socials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.socials
    ADD CONSTRAINT socials_pkey PRIMARY KEY (id);


--
-- Name: step_logs step_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.step_logs
    ADD CONSTRAINT step_logs_pkey PRIMARY KEY (id);


--
-- Name: store_locations store_locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_locations
    ADD CONSTRAINT store_locations_pkey PRIMARY KEY (id);


--
-- Name: store_payment_histories store_payment_histories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_payment_histories
    ADD CONSTRAINT store_payment_histories_pkey PRIMARY KEY (id);


--
-- Name: store_shipping_providers store_shipping_providers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_shipping_providers
    ADD CONSTRAINT store_shipping_providers_pkey PRIMARY KEY (id);


--
-- Name: stores stores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_pkey PRIMARY KEY (id);


--
-- Name: subcategories subcategories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories
    ADD CONSTRAINT subcategories_pkey PRIMARY KEY (id);


--
-- Name: user_sessions user_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_pkey PRIMARY KEY (id);


--
-- Name: user_sessions user_sessions_refresh_token_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_refresh_token_key UNIQUE (refresh_token);


--
-- Name: user_stores user_stores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_stores
    ADD CONSTRAINT user_stores_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_phone_number_key UNIQUE (phone_number);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: wards wards_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wards
    ADD CONSTRAINT wards_pkey PRIMARY KEY (id);


--
-- Name: workflow_steps workflow_steps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_steps
    ADD CONSTRAINT workflow_steps_pkey PRIMARY KEY (id);


--
-- Name: workflows workflows_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflows
    ADD CONSTRAINT workflows_pkey PRIMARY KEY (id);


--
-- Name: idx_subcategories_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_subcategories_category_id ON public.subcategories USING btree (category_id);


--
-- Name: idx_user_sessions_refresh_token; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_sessions_refresh_token ON public.user_sessions USING btree (refresh_token);


--
-- Name: idx_user_sessions_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_sessions_user_id ON public.user_sessions USING btree (user_id);


--
-- Name: idx_user_stores_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_stores_org_id ON public.user_stores USING btree (org_id);


--
-- Name: idx_user_stores_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_stores_store_id ON public.user_stores USING btree (store_id);


--
-- Name: idx_user_stores_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_stores_user_id ON public.user_stores USING btree (user_id);


--
-- Name: ix_ai_worker_skills_ai_worker_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ai_worker_skills_ai_worker_id ON public.ai_worker_skills USING btree (ai_worker_id);


--
-- Name: ix_ai_worker_skills_skill_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ai_worker_skills_skill_id ON public.ai_worker_skills USING btree (skill_id);


--
-- Name: ix_ai_worker_socials_ai_worker_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ai_worker_socials_ai_worker_id ON public.ai_worker_socials USING btree (ai_worker_id);


--
-- Name: ix_ai_worker_socials_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ai_worker_socials_org_id ON public.ai_worker_socials USING btree (org_id);


--
-- Name: ix_ai_worker_socials_social_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ai_worker_socials_social_id ON public.ai_worker_socials USING btree (social_id);


--
-- Name: ix_ai_worker_socials_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ai_worker_socials_user_id ON public.ai_worker_socials USING btree (user_id);


--
-- Name: ix_ai_worker_statistics_ai_worker_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ai_worker_statistics_ai_worker_id ON public.ai_worker_statistics USING btree (ai_worker_id);


--
-- Name: ix_ai_workers_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_ai_workers_store_id ON public.ai_workers USING btree (store_id);


--
-- Name: ix_audits_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_audits_org_id ON public.audits USING btree (org_id);


--
-- Name: ix_audits_record_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_audits_record_id ON public.audits USING btree (record_id);


--
-- Name: ix_audits_table_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_audits_table_name ON public.audits USING btree (table_name);


--
-- Name: ix_audits_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_audits_user_id ON public.audits USING btree (user_id);


--
-- Name: ix_bank_accounts_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_bank_accounts_store_id ON public.bank_accounts USING btree (store_id);


--
-- Name: ix_brands_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_brands_category_id ON public.brands USING btree (category_id);


--
-- Name: ix_brands_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_brands_org_id ON public.brands USING btree (org_id);


--
-- Name: ix_brands_subcategory_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_brands_subcategory_id ON public.brands USING btree (subcategory_id);


--
-- Name: ix_buyer_infos_buyer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_buyer_infos_buyer_id ON public.buyer_infos USING btree (buyer_id);


--
-- Name: ix_buyer_infos_product_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_buyer_infos_product_type_id ON public.buyer_infos USING btree (product_type_id);


--
-- Name: ix_buyer_infos_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_buyer_infos_store_id ON public.buyer_infos USING btree (store_id);


--
-- Name: ix_categories_product_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_categories_product_type_id ON public.categories USING btree (product_type_id);


--
-- Name: ix_communications_banners_display_position; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_communications_banners_display_position ON public.communications_banners USING btree (display_position);


--
-- Name: ix_communications_banners_end_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_communications_banners_end_date ON public.communications_banners USING btree (end_date);


--
-- Name: ix_communications_banners_start_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_communications_banners_start_date ON public.communications_banners USING btree (start_date);


--
-- Name: ix_conversations_ai_worker_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_conversations_ai_worker_id ON public.conversations USING btree (ai_worker_id);


--
-- Name: ix_conversations_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_conversations_org_id ON public.conversations USING btree (org_id);


--
-- Name: ix_conversations_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_conversations_user_id ON public.conversations USING btree (user_id);


--
-- Name: ix_departments_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_departments_name ON public.departments USING btree (name);


--
-- Name: ix_departments_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_departments_org_id ON public.departments USING btree (org_id);


--
-- Name: ix_districts_district_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_districts_district_code ON public.districts USING btree (district_code);


--
-- Name: ix_districts_province_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_districts_province_code ON public.districts USING btree (province_code);


--
-- Name: ix_keywords_keyword_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_keywords_keyword_name ON public.keywords USING btree (keyword_name);


--
-- Name: ix_keywords_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_keywords_slug ON public.keywords USING btree (slug);


--
-- Name: ix_knowledge_bases_ai_worker_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_knowledge_bases_ai_worker_id ON public.knowledge_bases USING btree (ai_worker_id);


--
-- Name: ix_knowledge_bases_aws_file_url; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_knowledge_bases_aws_file_url ON public.knowledge_bases USING btree (aws_file_url);


--
-- Name: ix_medias_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_medias_product_id ON public.medias USING btree (product_id);


--
-- Name: ix_membership_packages_package_title; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_membership_packages_package_title ON public.membership_packages USING btree (package_title);


--
-- Name: ix_membership_packages_price; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_membership_packages_price ON public.membership_packages USING btree (price);


--
-- Name: ix_messages_conversation_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_messages_conversation_id ON public.messages USING btree (conversation_id);


--
-- Name: ix_messages_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_messages_store_id ON public.messages USING btree (store_id);


--
-- Name: ix_notifications_is_read; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notifications_is_read ON public.notifications USING btree (is_read);


--
-- Name: ix_notifications_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notifications_org_id ON public.notifications USING btree (org_id);


--
-- Name: ix_notifications_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notifications_user_id ON public.notifications USING btree (user_id);


--
-- Name: ix_options_option_group_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_options_option_group_id ON public.options USING btree (option_group_id);


--
-- Name: ix_order_items_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_items_order_id ON public.order_items USING btree (order_id);


--
-- Name: ix_order_items_product_detail_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_items_product_detail_id ON public.order_items USING btree (product_detail_id);


--
-- Name: ix_order_items_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_items_product_id ON public.order_items USING btree (product_id);


--
-- Name: ix_order_payment_items_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_payment_items_order_id ON public.order_payment_items USING btree (order_id);


--
-- Name: ix_order_shipping_details_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_shipping_details_order_id ON public.order_shipping_details USING btree (order_id);


--
-- Name: ix_order_shipping_details_shipping_method_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_shipping_details_shipping_method_id ON public.order_shipping_details USING btree (shipping_method_id);


--
-- Name: ix_order_shipping_details_workflow_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_shipping_details_workflow_id ON public.order_shipping_details USING btree (workflow_id);


--
-- Name: ix_order_states_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_states_code ON public.order_states USING btree (code);


--
-- Name: ix_order_states_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_states_name ON public.order_states USING btree (name);


--
-- Name: ix_orders_buyer_info_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_buyer_info_id ON public.orders USING btree (buyer_info_id);


--
-- Name: ix_orders_cancel_reason_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_cancel_reason_id ON public.orders USING btree (cancel_reason_id);


--
-- Name: ix_orders_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_org_id ON public.orders USING btree (org_id);


--
-- Name: ix_orders_payment_method_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_payment_method_id ON public.orders USING btree (payment_method_id);


--
-- Name: ix_orders_product_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_product_type_id ON public.orders USING btree (product_type_id);


--
-- Name: ix_orders_state; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_state ON public.orders USING btree (state);


--
-- Name: ix_orders_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_store_id ON public.orders USING btree (store_id);


--
-- Name: ix_orders_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_user_id ON public.orders USING btree (user_id);


--
-- Name: ix_organization_memberships_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_organization_memberships_org_id ON public.organization_memberships USING btree (org_id);


--
-- Name: ix_organization_memberships_package_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_organization_memberships_package_id ON public.organization_memberships USING btree (package_id);


--
-- Name: ix_organizations_owner_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_organizations_owner_id ON public.organizations USING btree (owner_id);


--
-- Name: ix_payment_methods_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_payment_methods_name ON public.payment_methods USING btree (name);


--
-- Name: ix_payment_methods_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_payment_methods_type ON public.payment_methods USING btree (type);


--
-- Name: ix_permissions_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_permissions_name ON public.permissions USING btree (name);


--
-- Name: ix_product_details_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_details_category_id ON public.product_details USING btree (category_id);


--
-- Name: ix_product_details_keyword_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_details_keyword_id ON public.product_details USING btree (keyword_id);


--
-- Name: ix_product_details_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_details_product_id ON public.product_details USING btree (product_id);


--
-- Name: ix_product_details_product_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_details_product_type_id ON public.product_details USING btree (product_type_id);


--
-- Name: ix_product_details_sku_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_details_sku_code ON public.product_details USING btree (sku_code);


--
-- Name: ix_product_details_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_details_store_id ON public.product_details USING btree (store_id);


--
-- Name: ix_product_keywords_keyword_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_keywords_keyword_id ON public.product_keywords USING btree (keyword_id);


--
-- Name: ix_product_keywords_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_keywords_product_id ON public.product_keywords USING btree (product_id);


--
-- Name: ix_product_promotions_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_promotions_product_id ON public.product_promotions USING btree (product_id);


--
-- Name: ix_product_promotions_promotion_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_promotions_promotion_id ON public.product_promotions USING btree (promotion_id);


--
-- Name: ix_product_types_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_types_name ON public.product_types USING btree (name);


--
-- Name: ix_product_types_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_types_slug ON public.product_types USING btree (slug);


--
-- Name: ix_products_brand_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_brand_id ON public.products USING btree (brand_id);


--
-- Name: ix_products_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_category_id ON public.products USING btree (category_id);


--
-- Name: ix_products_flashsale_enddate; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_flashsale_enddate ON public.products USING btree (flashsale_enddate);


--
-- Name: ix_products_flashsale_startdate; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_flashsale_startdate ON public.products USING btree (flashsale_startdate);


--
-- Name: ix_products_is_flashsale; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_is_flashsale ON public.products USING btree (is_flashsale);


--
-- Name: ix_products_is_published; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_is_published ON public.products USING btree (is_published);


--
-- Name: ix_products_keyword_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_keyword_id ON public.products USING btree (keyword_id);


--
-- Name: ix_products_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_org_id ON public.products USING btree (org_id);


--
-- Name: ix_products_product_type_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_product_type_id ON public.products USING btree (product_type_id);


--
-- Name: ix_products_subcategory_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_subcategory_id ON public.products USING btree (subcategory_id);


--
-- Name: ix_promotions_end_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_promotions_end_date ON public.promotions USING btree (end_date);


--
-- Name: ix_promotions_start_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_promotions_start_date ON public.promotions USING btree (start_date);


--
-- Name: ix_promotions_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_promotions_store_id ON public.promotions USING btree (store_id);


--
-- Name: ix_provinces_province_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_provinces_province_code ON public.provinces USING btree (province_code);


--
-- Name: ix_receivers_buyer_info_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_receivers_buyer_info_id ON public.receivers USING btree (buyer_info_id);


--
-- Name: ix_reviews_customer_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reviews_customer_id ON public.reviews USING btree (customer_id);


--
-- Name: ix_reviews_entity_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reviews_entity_type ON public.reviews USING btree (entity_type);


--
-- Name: ix_reviews_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reviews_org_id ON public.reviews USING btree (org_id);


--
-- Name: ix_role_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_role_permissions_permission_id ON public.role_permissions USING btree (permission_id);


--
-- Name: ix_role_permissions_role_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_role_permissions_role_id ON public.role_permissions USING btree (role_id);


--
-- Name: ix_roles_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_roles_name ON public.roles USING btree (name);


--
-- Name: ix_setting_products_option_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_setting_products_option_id ON public.setting_products USING btree (option_id);


--
-- Name: ix_setting_products_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_setting_products_product_id ON public.setting_products USING btree (product_id);


--
-- Name: ix_shipping_infos_district_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_shipping_infos_district_code ON public.shipping_infos USING btree (district_code);


--
-- Name: ix_shipping_infos_province_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_shipping_infos_province_code ON public.shipping_infos USING btree (province_code);


--
-- Name: ix_shipping_infos_receiver_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_shipping_infos_receiver_id ON public.shipping_infos USING btree (receiver_id);


--
-- Name: ix_shipping_infos_ward_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_shipping_infos_ward_code ON public.shipping_infos USING btree (ward_code);


--
-- Name: ix_shipping_methods_shipping_provider_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_shipping_methods_shipping_provider_id ON public.shipping_methods USING btree (shipping_provider_id);


--
-- Name: ix_shipping_providers_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_shipping_providers_name ON public.shipping_providers USING btree (name);


--
-- Name: ix_skills_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_skills_name ON public.skills USING btree (name);


--
-- Name: ix_socials_platform; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_socials_platform ON public.socials USING btree (platform);


--
-- Name: ix_step_logs_delivery_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_step_logs_delivery_order_id ON public.step_logs USING btree (delivery_order_id);


--
-- Name: ix_step_logs_order_shipping_detail_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_step_logs_order_shipping_detail_id ON public.step_logs USING btree (order_shipping_detail_id);


--
-- Name: ix_step_logs_step_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_step_logs_step_id ON public.step_logs USING btree (step_id);


--
-- Name: ix_store_locations_district_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_locations_district_code ON public.store_locations USING btree (district_code);


--
-- Name: ix_store_locations_district_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_locations_district_id ON public.store_locations USING btree (district_id);


--
-- Name: ix_store_locations_province_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_locations_province_code ON public.store_locations USING btree (province_code);


--
-- Name: ix_store_locations_province_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_locations_province_id ON public.store_locations USING btree (province_id);


--
-- Name: ix_store_locations_ward_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_locations_ward_code ON public.store_locations USING btree (ward_code);


--
-- Name: ix_store_locations_ward_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_locations_ward_id ON public.store_locations USING btree (ward_id);


--
-- Name: ix_store_payment_histories_bank_account_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_payment_histories_bank_account_id ON public.store_payment_histories USING btree (bank_account_id);


--
-- Name: ix_store_payment_histories_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_payment_histories_org_id ON public.store_payment_histories USING btree (org_id);


--
-- Name: ix_store_payment_histories_payment_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_payment_histories_payment_date ON public.store_payment_histories USING btree (payment_date);


--
-- Name: ix_store_payment_histories_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_payment_histories_store_id ON public.store_payment_histories USING btree (store_id);


--
-- Name: ix_store_shipping_providers_shipping_provider_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_shipping_providers_shipping_provider_id ON public.store_shipping_providers USING btree (shipping_provider_id);


--
-- Name: ix_store_shipping_providers_store_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_store_shipping_providers_store_id ON public.store_shipping_providers USING btree (store_id);


--
-- Name: ix_stores_is_open; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_stores_is_open ON public.stores USING btree (is_open);


--
-- Name: ix_stores_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_stores_org_id ON public.stores USING btree (org_id);


--
-- Name: ix_stores_owner_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_stores_owner_id ON public.stores USING btree (owner_id);


--
-- Name: ix_stores_store_location_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_stores_store_location_id ON public.stores USING btree (store_location_id);


--
-- Name: ix_users_department_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_department_id ON public.users USING btree (department_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_is_verified; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_is_verified ON public.users USING btree (is_verified);


--
-- Name: ix_users_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_org_id ON public.users USING btree (org_id);


--
-- Name: ix_users_phone_number; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_phone_number ON public.users USING btree (phone_number);


--
-- Name: ix_users_role_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_role_id ON public.users USING btree (role_id);


--
-- Name: ix_wards_district_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_wards_district_code ON public.wards USING btree (district_code);


--
-- Name: ix_wards_province_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_wards_province_code ON public.wards USING btree (province_code);


--
-- Name: ix_wards_ward_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_wards_ward_code ON public.wards USING btree (ward_code);


--
-- Name: ix_workflow_steps_order_state_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_steps_order_state_id ON public.workflow_steps USING btree (order_state_id);


--
-- Name: ix_workflow_steps_order_workflow_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflow_steps_order_workflow_id ON public.workflow_steps USING btree (order_workflow_id);


--
-- Name: ix_workflows_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_workflows_name ON public.workflows USING btree (name);


--
-- Name: ai_worker_skills ai_worker_skills_ai_worker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_worker_skills
    ADD CONSTRAINT ai_worker_skills_ai_worker_id_fkey FOREIGN KEY (ai_worker_id) REFERENCES public.ai_workers(id) ON DELETE CASCADE;


--
-- Name: ai_worker_skills ai_worker_skills_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_worker_skills
    ADD CONSTRAINT ai_worker_skills_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.skills(id) ON DELETE CASCADE;


--
-- Name: ai_worker_socials ai_worker_socials_ai_worker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_worker_socials
    ADD CONSTRAINT ai_worker_socials_ai_worker_id_fkey FOREIGN KEY (ai_worker_id) REFERENCES public.ai_workers(id) ON DELETE CASCADE;


--
-- Name: ai_worker_socials ai_worker_socials_social_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_worker_socials
    ADD CONSTRAINT ai_worker_socials_social_id_fkey FOREIGN KEY (social_id) REFERENCES public.socials(id) ON DELETE CASCADE;


--
-- Name: ai_worker_statistics ai_worker_statistics_ai_worker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_worker_statistics
    ADD CONSTRAINT ai_worker_statistics_ai_worker_id_fkey FOREIGN KEY (ai_worker_id) REFERENCES public.ai_workers(id) ON DELETE CASCADE;


--
-- Name: ai_workers ai_workers_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ai_workers
    ADD CONSTRAINT ai_workers_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id) ON DELETE CASCADE;


--
-- Name: bank_accounts bank_accounts_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bank_accounts
    ADD CONSTRAINT bank_accounts_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id) ON DELETE CASCADE;


--
-- Name: cart_items cart_items_cart_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_cart_id_fkey FOREIGN KEY (cart_id) REFERENCES public.carts(id) ON DELETE CASCADE;


--
-- Name: categories categories_product_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_product_type_id_fkey FOREIGN KEY (product_type_id) REFERENCES public.product_types(id) ON DELETE CASCADE;


--
-- Name: conversations conversations_ai_worker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_ai_worker_id_fkey FOREIGN KEY (ai_worker_id) REFERENCES public.ai_workers(id) ON DELETE CASCADE;


--
-- Name: conversations conversations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.conversations
    ADD CONSTRAINT conversations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: knowledge_bases knowledge_bases_ai_worker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.knowledge_bases
    ADD CONSTRAINT knowledge_bases_ai_worker_id_fkey FOREIGN KEY (ai_worker_id) REFERENCES public.ai_workers(id) ON DELETE CASCADE;


--
-- Name: medias medias_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.medias
    ADD CONSTRAINT medias_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: messages messages_conversation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_conversation_id_fkey FOREIGN KEY (conversation_id) REFERENCES public.conversations(id) ON DELETE CASCADE;


--
-- Name: options options_option_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.options
    ADD CONSTRAINT options_option_group_id_fkey FOREIGN KEY (option_group_id) REFERENCES public.option_groups(id) ON DELETE CASCADE;


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: order_payment_items order_payment_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_payment_items
    ADD CONSTRAINT order_payment_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: order_shipping_details order_shipping_details_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_shipping_details
    ADD CONSTRAINT order_shipping_details_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- Name: order_shipping_details order_shipping_details_shipping_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_shipping_details
    ADD CONSTRAINT order_shipping_details_shipping_method_id_fkey FOREIGN KEY (shipping_method_id) REFERENCES public.shipping_methods(id) ON DELETE CASCADE;


--
-- Name: orders orders_buyer_info_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_buyer_info_id_fkey FOREIGN KEY (buyer_info_id) REFERENCES public.buyer_infos(id) ON DELETE CASCADE;


--
-- Name: orders orders_cancel_reason_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_cancel_reason_id_fkey FOREIGN KEY (cancel_reason_id) REFERENCES public.cancel_reasons(id) ON DELETE CASCADE;


--
-- Name: orders orders_payment_method_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_payment_method_id_fkey FOREIGN KEY (payment_method_id) REFERENCES public.payment_methods(id) ON DELETE CASCADE;


--
-- Name: organization_memberships organization_memberships_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_memberships
    ADD CONSTRAINT organization_memberships_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- Name: organization_memberships organization_memberships_package_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_memberships
    ADD CONSTRAINT organization_memberships_package_id_fkey FOREIGN KEY (package_id) REFERENCES public.membership_packages(id) ON DELETE CASCADE;


--
-- Name: product_details product_details_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_details
    ADD CONSTRAINT product_details_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: product_details product_details_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_details
    ADD CONSTRAINT product_details_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id) ON DELETE CASCADE;


--
-- Name: product_keywords product_keywords_keyword_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_keywords
    ADD CONSTRAINT product_keywords_keyword_id_fkey FOREIGN KEY (keyword_id) REFERENCES public.keywords(id) ON DELETE CASCADE;


--
-- Name: product_keywords product_keywords_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_keywords
    ADD CONSTRAINT product_keywords_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: product_promotions product_promotions_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_promotions
    ADD CONSTRAINT product_promotions_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: product_promotions product_promotions_promotion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_promotions
    ADD CONSTRAINT product_promotions_promotion_id_fkey FOREIGN KEY (promotion_id) REFERENCES public.promotions(id) ON DELETE CASCADE;


--
-- Name: products products_brand_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_brand_id_fkey FOREIGN KEY (brand_id) REFERENCES public.brands(id) ON DELETE CASCADE;


--
-- Name: products products_subcategory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_subcategory_id_fkey FOREIGN KEY (subcategory_id) REFERENCES public.subcategories(id) ON DELETE CASCADE;


--
-- Name: promotions promotions_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotions
    ADD CONSTRAINT promotions_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id) ON DELETE CASCADE;


--
-- Name: receivers receivers_buyer_info_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.receivers
    ADD CONSTRAINT receivers_buyer_info_id_fkey FOREIGN KEY (buyer_info_id) REFERENCES public.buyer_infos(id) ON DELETE CASCADE;


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id) ON DELETE CASCADE;


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: setting_products setting_products_option_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.setting_products
    ADD CONSTRAINT setting_products_option_id_fkey FOREIGN KEY (option_id) REFERENCES public.options(id) ON DELETE CASCADE;


--
-- Name: setting_products setting_products_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.setting_products
    ADD CONSTRAINT setting_products_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- Name: shipping_infos shipping_infos_receiver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipping_infos
    ADD CONSTRAINT shipping_infos_receiver_id_fkey FOREIGN KEY (receiver_id) REFERENCES public.receivers(id) ON DELETE CASCADE;


--
-- Name: shipping_methods shipping_methods_shipping_provider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipping_methods
    ADD CONSTRAINT shipping_methods_shipping_provider_id_fkey FOREIGN KEY (shipping_provider_id) REFERENCES public.shipping_providers(id) ON DELETE CASCADE;


--
-- Name: step_logs step_logs_order_shipping_detail_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.step_logs
    ADD CONSTRAINT step_logs_order_shipping_detail_id_fkey FOREIGN KEY (order_shipping_detail_id) REFERENCES public.order_shipping_details(id) ON DELETE CASCADE;


--
-- Name: step_logs step_logs_step_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.step_logs
    ADD CONSTRAINT step_logs_step_id_fkey FOREIGN KEY (step_id) REFERENCES public.workflow_steps(id) ON DELETE CASCADE;


--
-- Name: store_locations store_locations_district_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_locations
    ADD CONSTRAINT store_locations_district_id_fkey FOREIGN KEY (district_id) REFERENCES public.districts(id);


--
-- Name: store_locations store_locations_province_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_locations
    ADD CONSTRAINT store_locations_province_id_fkey FOREIGN KEY (province_id) REFERENCES public.provinces(id);


--
-- Name: store_locations store_locations_ward_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_locations
    ADD CONSTRAINT store_locations_ward_id_fkey FOREIGN KEY (ward_id) REFERENCES public.wards(id);


--
-- Name: store_payment_histories store_payment_histories_bank_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_payment_histories
    ADD CONSTRAINT store_payment_histories_bank_account_id_fkey FOREIGN KEY (bank_account_id) REFERENCES public.bank_accounts(id) ON DELETE CASCADE;


--
-- Name: store_payment_histories store_payment_histories_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_payment_histories
    ADD CONSTRAINT store_payment_histories_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- Name: store_payment_histories store_payment_histories_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_payment_histories
    ADD CONSTRAINT store_payment_histories_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id) ON DELETE CASCADE;


--
-- Name: store_shipping_providers store_shipping_providers_shipping_provider_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_shipping_providers
    ADD CONSTRAINT store_shipping_providers_shipping_provider_id_fkey FOREIGN KEY (shipping_provider_id) REFERENCES public.shipping_providers(id) ON DELETE CASCADE;


--
-- Name: store_shipping_providers store_shipping_providers_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_shipping_providers
    ADD CONSTRAINT store_shipping_providers_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id) ON DELETE CASCADE;


--
-- Name: stores stores_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_org_id_fkey FOREIGN KEY (org_id) REFERENCES public.organizations(id) ON DELETE CASCADE;


--
-- Name: stores stores_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: stores stores_store_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_store_location_id_fkey FOREIGN KEY (store_location_id) REFERENCES public.store_locations(id) ON DELETE CASCADE;


--
-- Name: subcategories subcategories_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subcategories
    ADD CONSTRAINT subcategories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE;


--
-- Name: user_sessions user_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: user_stores user_stores_store_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_stores
    ADD CONSTRAINT user_stores_store_id_fkey FOREIGN KEY (store_id) REFERENCES public.stores(id) ON DELETE CASCADE;


--
-- Name: user_stores user_stores_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_stores
    ADD CONSTRAINT user_stores_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: users users_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.departments(id) ON DELETE SET NULL;


--
-- Name: users users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: workflow_steps workflow_steps_order_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_steps
    ADD CONSTRAINT workflow_steps_order_state_id_fkey FOREIGN KEY (order_state_id) REFERENCES public.order_states(id) ON DELETE CASCADE;


--
-- Name: workflow_steps workflow_steps_order_workflow_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workflow_steps
    ADD CONSTRAINT workflow_steps_order_workflow_id_fkey FOREIGN KEY (order_workflow_id) REFERENCES public.workflows(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

