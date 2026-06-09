# Multi-Country Waste Collection Platform - Web Flow & Panel Design

## 1. Product Direction

The product should be designed as an operations-first, Uber-style waste collection marketplace for Ghana first, with expansion support for Nigeria and Côte d'Ivoire. The platform does not depend on company-owned trucks or collectors; instead, independent collectors register, get approved, receive pickup jobs, upload proof, and get paid.

Phase 1 should prioritize the web-based operations dashboard before the mobile app, because dispatching, collector approval, sack verification, payment monitoring, and reporting are the business-critical workflows.

## 2. Recommended Technology Stack

| Layer | Recommended Stack | Reason |
| --- | --- | --- |
| Web frontend | Next.js, TypeScript, Tailwind CSS, shadcn/ui | Fast dashboard development, server-rendered pages, role-based layouts, reusable components |
| Backend API | Node.js with NestJS or Express.js, TypeScript | Scalable REST/GraphQL APIs, background jobs, integrations, role-based access control |
| Database | PostgreSQL with PostGIS | Reliable relational data, multi-country records, geo queries for nearest collectors |
| Cache and queues | Redis + BullMQ | Auto-dispatch jobs, SMS processing, webhook retries, payout jobs |
| File storage | S3-compatible object storage | Pickup proof photos, collector documents, customer sack images |
| Maps and tracking | Google Maps, Mapbox, or OpenStreetMap | Collector location display, pickup zones, nearest collector matching |
| SMS gateway | Africa's Talking, Twilio, Hubtel, or local Ghana SMS provider | Feature-phone booking and status notifications |
| Payments | Paystack, Flutterwave, Hubtel, MTN MoMo integrations | Ghana MoMo priority, cards, bank transfer, wallets, multi-country expansion |

## 3. Web Panels to Build Separately

### 3.1 Super Admin Panel

Purpose: control countries, platform settings, pricing, integrations, and global reporting.

Core screens:

1. Country management
   - Ghana, Nigeria, Côte d'Ivoire setup
   - Currency, timezone, tax rules, language, city zones
   - Payment provider configuration per country
2. Role and permission management
   - Super admin, country admin, dispatcher, finance, support, inventory manager
   - Permission matrix for viewing, assigning, refunding, approving, and exporting data
3. Platform configuration
   - Pickup statuses
   - Collector commission rules
   - Customer fees
   - Cancellation rules
   - SMS templates
4. Global reports
   - Country-by-country pickups
   - Revenue by country
   - Collector growth
   - Customer growth
   - Sack sales and usage

### 3.2 Country Operations Admin Panel

Purpose: daily operations command center for each launch country.

Core screens:

1. Operations dashboard
   - Total requests today
   - Pending pickups
   - Assigned pickups
   - Completed pickups
   - Cancelled pickups
   - Active collectors online
   - Revenue collected today
2. Pickup request management
   - View all customer requests
   - Filter by city, zone, status, sack count, time slot, payment status
   - Open request detail view
   - Assign or reassign collector
   - Cancel, reschedule, or escalate request
3. Manual assignment
   - Select pickup request
   - View available collectors by zone and current status
   - Assign collector manually
   - Override auto-dispatch when needed
4. Automatic assignment monitor
   - View system-suggested collector
   - See matching reason: nearest, online, capacity, rating, acceptance rate
   - Approve or override assignment
5. Live tracking
   - Map of active collectors
   - Current collector location
   - Active job route and pickup progress
   - Last location update timestamp
6. Proof verification
   - Review completion photo
   - Confirm official company sacks were collected
   - Flag disputed or unclear pickups
   - Mark job verified for payout
7. Reporting
   - Daily and weekly pickup reports
   - Collector performance
   - Customer activity
   - Payment collection report
   - Cancellation and dispute report

### 3.3 Collector Management Panel

Purpose: onboard, approve, monitor, and manage independent collectors.

Core screens:

1. Collector applications
   - New registrations
   - Identity information
   - Vehicle or transport type
   - Service zones
   - Uploaded documents
   - Approve, reject, or request more information
2. Collector profile
   - Contact details
   - Country, city, zones
   - Online/offline status
   - Current active job
   - Completed jobs
   - Ratings and complaints
3. Performance tracking
   - Acceptance rate
   - Completion rate
   - Average pickup time
   - Proof photo compliance
   - Disputes and cancellations
4. Earnings and payouts
   - Total earned
   - Pending payout
   - Paid payout
   - Deductions
   - Payment method
5. Collector status control
   - Temporarily suspend collector
   - Deactivate collector
   - Reassign collector zones
   - Manual status override for emergency operations

### 3.4 Customer Support Panel

Purpose: help smartphone and SMS customers without giving support agents full admin access.

Core screens:

1. Customer search
   - Search by phone, name, email, customer ID, or SMS sender number
2. Customer profile
   - Pickup history
   - Sack purchase history
   - Wallet balance
   - Payment history
   - Complaints and support notes
3. Request assistance
   - Create pickup request on behalf of customer
   - Reschedule pickup
   - Cancel pickup
   - Add notes for dispatcher
4. Dispute handling
   - View customer complaint
   - View collector proof photo
   - Escalate to operations admin
   - Record resolution

### 3.5 Sack Inventory and Pricing Panel

Purpose: manage the official company sack model, which is central to the business.

Core screens:

1. Sack catalog
   - Small sack
   - Medium sack
   - Large sack
   - Price per country and currency
   - Active/inactive status
2. Sack inventory
   - Stock by country, city, and warehouse
   - Stock assigned to agents or collectors
   - Low-stock alerts
3. Sack sales
   - Customer sack purchases
   - Payment status
   - Delivery or pickup method
4. Sack validation rules
   - Collect only company-issued sacks
   - Optional QR code or batch code support
   - Flag non-company sacks in proof verification
5. Regular pickup pricing
   - Fixed price by number of sacks
   - No distance pricing for regular collection
   - Country-specific price tables
6. Special pickup pricing
   - Furniture
   - Construction waste
   - Bulk collection
   - Manual quote and approval workflow

### 3.6 Finance and Payments Panel

Purpose: monitor payments, wallets, cash collection, and collector payouts.

Core screens:

1. Payment overview
   - Successful payments
   - Pending payments
   - Failed payments
   - Cash collections
   - Wallet payments
2. Mobile money monitoring
   - MTN MoMo
   - Vodafone Cash
   - AirtelTigo Money
   - Provider reference number
   - Webhook status
3. Bank and card payments
   - Card transactions
   - Bank transfers
   - Manual reconciliation queue
4. Wallet ledger
   - Customer wallet credits
   - Customer wallet debits
   - Refunds
   - Adjustments
5. Collector payouts
   - Jobs verified for payout
   - Payout pending
   - Payout completed
   - Failed payout retry
6. Cash and digital hybrid flow
   - Cash received by collector
   - Digital payment partial balance
   - Wallet top-up or wallet deduction
   - Admin reconciliation before payout

### 3.7 SMS Booking Panel

Purpose: manage feature-phone requests and failed SMS parsing.

Core screens:

1. Incoming SMS inbox
   - Sender phone number
   - Message body
   - Parsed intent
   - Country and city detection
   - Processing status
2. Parsed pickup requests
   - Example: `PICKUP 3 SACKS`
   - Sack count
   - Customer phone
   - Preferred time slot
   - Address confirmation status
3. Manual SMS correction queue
   - Unrecognized messages
   - Missing address
   - Missing sack count
   - Support agent correction
4. SMS templates
   - Booking confirmation
   - Collector assigned
   - Pickup completed
   - Payment reminder
   - Failed booking instructions

### 3.8 Analytics Panel

Purpose: give management a clear view of growth and efficiency.

Core screens:

1. Operational analytics
   - Pickup volume by day, week, month
   - Pickup status distribution
   - Average completion time
   - Cancelled request reasons
2. Revenue analytics
   - Revenue by country
   - Revenue by city
   - Revenue by sack size
   - Revenue by payment method
3. Collector analytics
   - Top collectors
   - Low-performing collectors
   - Zone coverage gaps
   - Online collector supply by hour
4. Customer analytics
   - New customers
   - Repeat customers
   - SMS vs app bookings
   - Customer lifetime value

## 4. Customer Web Flow

Although the mobile app can come later, the web platform should include a customer web panel or responsive portal for early launch and admin-assisted operations.

Flow:

1. Customer registers with phone number, name, country, city, and address.
2. Customer buys official company sacks or confirms they already have approved sacks.
3. Customer creates a regular pickup request by selecting:
   - Number of sacks
   - Sack sizes
   - Pickup address
   - Morning, afternoon, or evening time slot
   - Payment method
4. System calculates fixed sack-based price.
5. Customer pays by mobile money, card, wallet, bank transfer, or cash option if enabled.
6. Request enters pending queue.
7. Admin manually assigns collector in Phase 1.
8. Collector picks up sacks and uploads proof photo.
9. Customer receives completion notification and can view proof.
10. Customer can rate service or open a dispute.

## 5. Collector Web Flow

The primary collector experience should eventually live inside the single Flutter app, but a web collector portal is useful for early operations and internal testing.

Flow:

1. Collector registers with phone, country, city, zones, ID details, and payout method.
2. Admin reviews and approves collector.
3. Collector switches online.
4. Collector receives assigned job.
5. Collector accepts or rejects job.
6. Collector moves through statuses:
   - Assigned
   - Accepted
   - On the way
   - Arrived
   - Collected
   - Completed
7. Collector uploads proof photo showing official company sacks.
8. Admin verifies proof if required.
9. Collector earnings are added to payout queue.

## 6. Pickup Status Flow

Recommended status lifecycle:

1. Draft
2. Pending payment
3. Payment confirmed
4. Pending assignment
5. Assigned
6. Accepted by collector
7. Collector on the way
8. Collector arrived
9. Collected
10. Proof uploaded
11. Completed
12. Verified
13. Paid out

Exception statuses:

- Cancelled by customer
- Cancelled by admin
- Rejected by collector
- No collector available
- Disputed
- Refunded
- Failed payment
- Rescheduled

## 7. Automatic Assignment Logic

Phase 1 can use manual assignment only, but the data model should be ready for auto-dispatch.

Suggested matching rules:

1. Pickup country and city must match collector service country and city.
2. Collector must be approved and online.
3. Collector must be inside or near the pickup zone.
4. Collector must not exceed active job limit.
5. Collector score should consider:
   - Distance from pickup
   - Acceptance rate
   - Completion rate
   - Rating
   - Current workload
   - Recent cancellations
6. System assigns the best collector or creates a ranked shortlist for admin approval.
7. Admin can override assignment at any time.

## 8. Suggested Database Modules

Use PostgreSQL as the primary database. Add PostGIS when live tracking and nearest-collector assignment are implemented.

Core tables:

- countries
- cities
- zones
- users
- roles
- permissions
- customers
- collectors
- collector_documents
- collector_locations
- sack_types
- sack_inventory
- sack_orders
- pickup_requests
- pickup_request_items
- pickup_assignments
- pickup_status_history
- proof_photos
- payments
- wallets
- wallet_transactions
- collector_earnings
- payouts
- sms_messages
- support_tickets
- disputes
- audit_logs

## 9. API Modules for Node.js Backend

Recommended backend modules:

1. Auth module
   - Login
   - Phone OTP
   - Role-based access control
2. Country configuration module
   - Countries
   - Currencies
   - Payment providers
3. Customer module
   - Profiles
   - Addresses
   - Activity history
4. Collector module
   - Applications
   - Approvals
   - Documents
   - Online status
   - Locations
5. Pickup module
   - Regular pickup requests
   - Special pickup requests
   - Status updates
   - Assignment
   - Proof upload
6. Sack module
   - Sack catalog
   - Inventory
   - Sack orders
   - Sack-based pricing
7. Payment module
   - MoMo
   - Cards
   - Bank transfer
   - Wallet
   - Cash reconciliation
8. SMS module
   - Incoming SMS parser
   - Outgoing notifications
   - Manual correction queue
9. Reporting module
   - Operational reports
   - Revenue reports
   - Collector reports
   - Customer reports
10. Notification module
   - SMS
   - Email
   - Push notification
   - WhatsApp later if required

## 10. Development Phases

### Phase 1 - Operations Dashboard

Build first:

- Admin login
- Country-ready structure
- Pickup request management
- Collector onboarding and approval
- Manual job assignment
- Sack inventory and pricing management
- Photo proof verification
- Payment monitoring
- Basic reporting
- Foundation for future auto-dispatch

### Phase 2 - Core Customer and Collector App

Build second:

- Single Flutter app with role-based access
- Customer registration
- Collector registration
- Customer pickup requests
- Collector job acceptance and status updates
- Customer pickup history
- Collector earnings view

### Phase 3 - Payments and SMS

Build third:

- Ghana MoMo integrations
- Card payments
- Bank transfer reconciliation
- Wallet balance
- Cash and digital hybrid handling
- SMS booking parser
- SMS notifications

### Phase 4 - Automation and Scaling

Build fourth:

- Automatic nearest-collector assignment
- Live tracking dashboard
- Advanced analytics
- Multi-country rollout
- Special pickup quoting workflow
- QR or batch validation for official sacks

## 11. Next.js Route Structure

Suggested frontend route structure:

```text
/app
  /(auth)/login
  /(auth)/forgot-password
  /(super-admin)/countries
  /(super-admin)/settings
  /(super-admin)/reports
  /(operations)/dashboard
  /(operations)/pickups
  /(operations)/pickups/[id]
  /(operations)/assignments
  /(operations)/tracking
  /(collectors)/applications
  /(collectors)/profiles/[id]
  /(collectors)/performance
  /(inventory)/sacks
  /(inventory)/orders
  /(finance)/payments
  /(finance)/wallets
  /(finance)/payouts
  /(support)/customers
  /(support)/tickets
  /(sms)/inbox
  /(sms)/templates
  /(analytics)/overview
  /(customer)/dashboard
  /(customer)/pickups
  /(collector)/jobs
  /(collector)/earnings
```

## 12. Minimum Viable Phase 1 Scope

For the first paid milestone, describe the Fiverr offer as:

**Phase 1 - Operations Dashboard for Waste Collection Platform**

Includes:

- Admin login and role-based dashboard
- Pickup request management
- Collector onboarding and approval
- Manual job assignment
- Official sack inventory and pricing management
- Photo proof verification
- Payment monitoring screen
- Daily and weekly reporting dashboard
- Database foundation for Ghana, Nigeria, and Côte d'Ivoire
- Backend foundation for future auto-dispatch, SMS booking, and mobile app integration
