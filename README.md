# PhD & Postdoc Research Network Website

A clean, responsive website for your informal PhD and postdoc association, designed to showcase your workshops and conferences.

## Features

- 📱 Fully responsive design (works on mobile, tablet, and desktop)
- 🎨 Modern, professional appearance
- 📅 Dedicated pages for each event with detailed information
- 📝 Easy-to-update structure
- 🚀 Ready to deploy on GitHub Pages

## File Structure

```
├── index.html              # Homepage
├── events.html             # List of all events
├── about.html              # About the association
├── contact.html            # Contact information
├── styles.css              # All styling
├── events/                 # Folder for individual event pages
│   ├── summer-2025.html    # Example: upcoming event
│   ├── winter-2024.html    # Example: past event (create as needed)
│   └── event-template.html # Template for new events
└── README.md              # This file
```

## Deploying to GitHub Pages

### Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository (e.g., "phd-network-website")
5. Make it **Public**
6. Don't initialize with README (you already have one)
7. Click "Create repository"

### Step 2: Upload Your Files

**Option A: Using Git (Recommended)**

```bash
# Navigate to your website folder
cd path/to/your/website

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial website commit"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Option B: Using GitHub Web Interface**

1. On your repository page, click "uploading an existing file"
2. Drag and drop all your website files
3. Click "Commit changes"

### Step 3: Enable GitHub Pages

1. In your repository, go to **Settings**
2. Scroll down to **Pages** section (in the left sidebar)
3. Under "Source", select **Deploy from a branch**
4. Under "Branch", select **main** and folder **/root**
5. Click **Save**
6. Wait a few minutes for deployment

Your site will be available at: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`

## Customizing the Website

### Updating Site Name and Branding

1. Open each HTML file
2. Find `<h1>PhD & Postdoc Network</h1>` in the navigation
3. Replace with your association's name
4. Update the `<title>` tags in each page header

### Changing Colors

Edit `styles.css`:

- **Primary color** (purple gradient): Find `.hero` section
- **Navigation bar**: Find `.navbar` section (currently `#2c3e50`)
- **Accent color**: Find `.btn-secondary` (currently `#3498db`)

### Adding Your Logo

1. Add your logo image to the root folder (e.g., `logo.png`)
2. In each HTML file, add to the nav-brand section:
```html
<div class="nav-brand">
    <img src="logo.png" alt="Logo" style="height: 40px; margin-right: 10px;">
    <h1>Your Association Name</h1>
</div>
```

## Adding a New Event

### Step 1: Create Event Page

1. Copy `events/event-template.html`
2. Rename it (e.g., `events/spring-2026.html`)
3. Open the file and replace all placeholders:
   - `[EVENT NAME]` - Your event title
   - `[DATE RANGE]` - Event dates
   - `[VENUE]` - Location
   - Add schedule items, speakers, registration info, etc.

### Step 2: Add Event to Events List

1. Open `events.html`
2. Add a new event card in the appropriate section (Upcoming or Past):

```html
<div class="event-card">
    <div class="event-header">
        <div>
            <h3 class="event-title">Your Event Name</h3>
            <p class="event-date">📅 Date | 📍 Venue</p>
        </div>
        <span class="event-badge badge-upcoming">Upcoming</span>
    </div>
    <p class="event-description">
        Brief description of your event...
    </p>
    <a href="events/your-event.html" class="btn btn-secondary">View Details & Register</a>
</div>
```

### Step 3: Update Homepage (Optional)

If you want to feature the event on the homepage:
1. Open `index.html`
2. Update the "Latest News" section

## Setting Up Event Registration

The website includes placeholder registration buttons. To make them functional, you have several options:

### Option 1: Google Forms (Easiest)
1. Create a Google Form for registration
2. Replace the `#` in the registration button with your Google Form link:
```html
<a href="https://forms.gle/YOUR-FORM-ID" class="btn btn-primary">Register Now</a>
```

### Option 2: Eventbrite
1. Create an event on Eventbrite
2. Link the registration button to your Eventbrite event page

### Option 3: Email Registration
```html
<a href="mailto:registration@yourassociation.org?subject=Workshop Registration" class="btn btn-primary">Register via Email</a>
```

## Setting Up the Contact Form

The contact form is currently static. To make it functional:

### Option 1: Formspree (Free, Easy)
1. Go to [Formspree.io](https://formspree.io)
2. Sign up for free account
3. Create a new form
4. Update the form tag in `contact.html`:
```html
<form action="https://formspree.io/f/YOUR-FORM-ID" method="POST">
```

### Option 2: Google Forms
1. Create a Google Form
2. Replace the entire form section with an embedded Google Form iframe

## Updating Content

### Homepage Updates
- **Hero section**: Edit `index.html`, find the `<header class="hero">` section
- **News**: Update the "Latest News" section in `index.html`

### About Page
- Edit `about.html` to customize your association's story and mission

### Contact Information
- Edit `contact.html` to update email addresses, social media links, etc.

## Tips for Maintenance

1. **Keep it simple**: Don't overcomplicate the design
2. **Regular updates**: Update the events page after each event
3. **Archive old events**: Move past events to the "Past Events" section
4. **Test responsiveness**: Check how the site looks on mobile devices
5. **Update dates**: Keep "Important Dates" sections current

## Making Updates After Initial Deployment

### Using Git:
```bash
# Make your changes to the files
# Then:
git add .
git commit -m "Description of changes"
git push
```

### Using GitHub Web Interface:
1. Navigate to the file you want to edit
2. Click the pencil icon (Edit)
3. Make your changes
4. Scroll down and click "Commit changes"

Changes will appear on your live site within a few minutes.

## Troubleshooting

### Site not loading?
- Check that GitHub Pages is enabled in Settings
- Ensure you selected the correct branch (main) and folder (root)
- Wait 5-10 minutes after initial deployment

### Links not working?
- Make sure file paths are correct
- For event pages, links should be `events/event-name.html`
- For images, use relative paths like `images/photo.jpg`

### Styles not appearing?
- Check that `styles.css` is in the root folder
- Verify the link in HTML: `<link rel="stylesheet" href="styles.css">`

## Customization Ideas

- Add an image gallery from past events
- Include speaker bios
- Add a blog or news section
- Create a resources page for members
- Add participant testimonials
- Include links to published proceedings

## Support

For issues with:
- **GitHub Pages**: Check [GitHub Pages documentation](https://docs.github.com/en/pages)
- **HTML/CSS questions**: [MDN Web Docs](https://developer.mozilla.org/)
- **Git help**: [Git documentation](https://git-scm.com/doc)

## License

Feel free to use and modify this template for your association's needs!

---

**Need help?** The template is designed to be beginner-friendly, but if you get stuck, consider asking a tech-savvy colleague or checking the GitHub Pages documentation.

Good luck with your website! 🎉
