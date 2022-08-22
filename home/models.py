from django.db import models
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailmedia.edit_handlers import MediaChooserPanel


class HomePage(Page):
    side_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')
    about_us_title = models.CharField(blank=True, max_length=250)
    short_description = models.CharField(blank=True, max_length=200)
    vision = models.CharField(blank=True, max_length=2000)
    vision_icon_class = models.CharField(blank=True, max_length=250)
    mission = models.CharField(blank=True, max_length=2000)
    mission_icon_class = models.CharField(blank=True, max_length=250)
    annual_beneficiary_count = models.CharField(blank=True, max_length=100)

    content_panels = Page.content_panels + [
        InlinePanel('carousel_items', label="Carousel items"),
        ImageChooserPanel('side_image'),
        FieldPanel('about_us_title'),
        FieldPanel('short_description'),
        FieldPanel('vision'),
        FieldPanel('vision_icon_class'),
        FieldPanel('mission'),
        FieldPanel('mission_icon_class'),
        InlinePanel('statistics_items', label="current Statistics"),
        InlinePanel('work_items', label="what we do"),
        InlinePanel('inclusion_items', label="Get involved"),
        FieldPanel('annual_beneficiary_count'),
    ]


class HomePageCarousel(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE,
                       related_name='carousel_items')
    featured_photo = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    featured_photo_title = models.CharField(blank=True, max_length=250)
    caption = models.CharField(blank=True, max_length=800)
    quick_link = models.CharField(blank=True, max_length=250)
    panels = [ImageChooserPanel('featured_photo'),
              FieldPanel('featured_photo_title'),
              FieldPanel('caption'),
              FieldPanel('quick_link'),
              ]


class HomePageStatistics(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE,
                       related_name='statistics_items')
    title = models.CharField(blank=True, max_length=250)
    icon_class = models.CharField(blank=True, max_length=250)
    number = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('title'),
        FieldPanel('icon_class'),
        FieldPanel('number'),
    ]


class HomePageWork(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE,
                       related_name='work_items')
    title = models.CharField(blank=True, max_length=250)
    cause_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    description = models.CharField(blank=True, max_length=2000)
    link = models.CharField(blank=True, max_length=250)
    panels = [
        FieldPanel('title'),
        ImageChooserPanel('cause_image'),
        FieldPanel('description'),
        FieldPanel('link'),
    ]


class HomePageInclusion(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE,
                       related_name='inclusion_items')
    title = models.CharField(blank=True, max_length=250)
    description = models.CharField(blank=True, max_length=2000)
    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
    ]


class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    thank_you_message = RichTextField(blank=True, null=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel(
            'intro', help_text="Add the introductory text for the contact page."),
        FieldPanel('location', help_text="contact physical location"),
        FieldPanel('email', help_text="Contact Email address"),
        FieldPanel('phone', help_text="Contact Phone number"),
        InlinePanel('form_fields', label="Contact form Sections",
                    help_text="form fields"),
        FieldPanel('thank_you_message',
                   help_text="This is the thank you text after successful submission."),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], heading="Email Settings"),
    ]


class ContactPageFormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE,
                       related_name='form_fields')


class GalleryPage(Page):
    page_title = models.CharField(blank=True, max_length=250)
    short_description = models.CharField(blank=True, max_length=200)

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('short_description'),
        InlinePanel('gallery_images', label="Gallery Images ",
                    max_num=18, min_num=3)
    ]


class GalleryPageGalleryImage(Orderable):
    page = ParentalKey(GalleryPage, on_delete=models.CASCADE,
                       related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    tag = models.CharField(blank=True, max_length=250,
                           help_text="Image Tag, eg ALP, CPTA, WETP, etc.")
    caption = models.CharField(blank=True, max_length=250)
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('tag'),
        FieldPanel('caption'),
    ]


class AboutPage(Page):
    side_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')
    about_us_title = models.CharField(blank=True, max_length=250)
    about_us_narration = models.CharField(blank=True, max_length=2000)
    about_us_body = RichTextField(blank=True, null=True)
    vision = models.CharField(blank=True, max_length=2000)
    purpose_statement = models.CharField(blank=True, max_length=2000)

    content_panels = Page.content_panels + [
        ImageChooserPanel('side_image'),
        FieldPanel('about_us_title'),
        FieldPanel('about_us_narration'),
        FieldPanel('about_us_body'),
        FieldPanel('vision'),
        FieldPanel('purpose_statement'),
        InlinePanel('organogram_items', label="Team Structure"),
        InlinePanel('values_items', label="values & aims "),
        InlinePanel('objective_items', label="Objectives"),
    ]


class AboutPageOrganogram(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE,
                       related_name='organogram_items')
    title = models.CharField(blank=True, max_length=250)
    designation = models.CharField(blank=True, max_length=2000)
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.CASCADE, related_name='+')
    facebook_link = models.CharField(blank=True, max_length=250)
    twitter_link = models.CharField(blank=True, max_length=250)
    linkedIn_link = models.CharField(blank=True, max_length=250)
    panels = [
        ImageChooserPanel('image'),
        FieldPanel('title'),
        FieldPanel('designation'),
        FieldPanel('facebook_link'),
        FieldPanel('twitter_link'),
        FieldPanel('linkedIn_link'),
    ]


class AboutPageValues(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE,
                       related_name='values_items')
    title = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('title'),

    ]


class AboutPageObjectives(Orderable):
    page = ParentalKey(AboutPage, on_delete=models.CASCADE,
                       related_name='objective_items')
    title = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('title'),
    ]


class EctpPage(Page):
    feature_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')
    side_title = models.CharField(blank=True, max_length=250)
    side_description = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('feature_image'),
        FieldPanel('side_title'),
        FieldPanel('side_description'),
        InlinePanel('carousel_items', label="ECTP Carousel Image",
                    help_text="ECTP slide Images"),
        InlinePanel('faqs', label="ECTP FAQs",
                    help_text="Frequently Asked Questions about ECTP"),
    ]


class EctpPageCarousel(Orderable):
    page = ParentalKey(EctpPage, on_delete=models.CASCADE,
                       related_name='carousel_items')
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.CASCADE, related_name='+')
    panels = [
        ImageChooserPanel('image'),
    ]


class EctpPageFaqs(Orderable):
    page = ParentalKey(EctpPage, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(blank=True, max_length=250)
    answer = models.CharField(blank=True, max_length=2000)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]


class CptaPage(Page):
    feature_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')
    side_title = models.CharField(blank=True, max_length=250)
    side_description = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('feature_image'),
        FieldPanel('side_title'),
        FieldPanel('side_description'),
        InlinePanel('carousel_items', label="CPTA Carousel Image",
                    help_text="CPTA slide Images"),
        InlinePanel('faqs', label="CPTA FAQs",
                    help_text="Frequently Asked Questions about CPTA"),
    ]


class CptaPageCarousel(Orderable):
    page = ParentalKey(CptaPage, on_delete=models.CASCADE,
                       related_name='carousel_items')
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.CASCADE, related_name='+')
    panels = [
        ImageChooserPanel('image'),
    ]


class CptaPageFaqs(Orderable):
    page = ParentalKey(CptaPage, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(blank=True, max_length=250)
    answer = models.CharField(blank=True, max_length=2000)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]


class WetcpPage(Page):
    feature_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')
    side_title = models.CharField(blank=True, max_length=250)
    side_description = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('feature_image'),
        FieldPanel('side_title'),
        FieldPanel('side_description'),
        InlinePanel('carousel_items', label="WETCP Carousel Image",
                    help_text="WETCP slide Images"),
        InlinePanel('faqs', label="WETCP FAQs",
                    help_text="Frequently Asked Questions about WETCP"),
    ]


class WetcpPageCarousel(Orderable):
    page = ParentalKey(WetcpPage, on_delete=models.CASCADE,
                       related_name='carousel_items')
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.CASCADE, related_name='+')
    panels = [
        ImageChooserPanel('image'),
    ]


class WetcpPageFaqs(Orderable):
    page = ParentalKey(WetcpPage, on_delete=models.CASCADE,
                       related_name='faqs')
    question = models.CharField(blank=True, max_length=250)
    answer = models.CharField(blank=True, max_length=2000)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]


class CepPage(Page):
    feature_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')
    side_title = models.CharField(blank=True, max_length=250)
    side_description = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('feature_image'),
        FieldPanel('side_title'),
        FieldPanel('side_description'),
        InlinePanel('carousel_items', label="CEP Carousel Image",
                    help_text="CEP slide Images"),
        InlinePanel('faqs', label="CEP FAQs",
                    help_text="Frequently Asked Questions about CEP"),
    ]


class CepPageCarousel(Orderable):
    page = ParentalKey(CepPage, on_delete=models.CASCADE,
                       related_name='carousel_items')
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.CASCADE, related_name='+')
    panels = [
        ImageChooserPanel('image'),
    ]


class CepPageFaqs(Orderable):
    page = ParentalKey(CepPage, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(blank=True, max_length=250)
    answer = models.CharField(blank=True, max_length=2000)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]


class AlpPage(Page):
    feature_image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, related_name='+')
    side_title = models.CharField(blank=True, max_length=250)
    side_description = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('feature_image'),
        FieldPanel('side_title'),
        FieldPanel('side_description'),
        InlinePanel('carousel_items', label="ALP Carousel Image",
                    help_text="ALP slide Images"),
        InlinePanel('faqs', label="ALP FAQs",
                    help_text="Frequently Asked Questions about ALP"),
    ]


class AlpPageCarousel(Orderable):
    page = ParentalKey(AlpPage, on_delete=models.CASCADE,
                       related_name='carousel_items')
    image = models.ForeignKey('wagtailimages.Image',
                              on_delete=models.CASCADE, related_name='+')
    panels = [
        ImageChooserPanel('image'),
    ]


class AlpPageFaqs(Orderable):
    page = ParentalKey(AlpPage, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(blank=True, max_length=250)
    answer = models.CharField(blank=True, max_length=2000)
    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]


class DonatePage(AbstractEmailForm):
    side_ttle = models.CharField(max_length=255, blank=True, null=True)

    hero_image = models.ForeignKey('wagtailimages.Image', null=True, on_delete=models.SET_NULL, related_name='+')
    side_body = RichTextField(blank=True, null=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('side_ttle'),
        FieldPanel('side_body'),
        ImageChooserPanel('hero_image'),
        InlinePanel('form_fields', label="Donate form Fields",
                    help_text="form fields"),
        FieldPanel('thank_you_text'),
    ]


class DonateFormField(AbstractFormField):
    page = ParentalKey(
        'DonatePage', related_name='form_fields', on_delete=models.CASCADE)


class TermsOfServicePage(Page):
    page_title = models.CharField(max_length=255, blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    body = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('introduction'),
        FieldPanel('body')
    ]


class PrivacyPolicyPage(Page):
    page_title = models.CharField(max_length=255, blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    body = RichTextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('page_title'),
        FieldPanel('introduction'),
        FieldPanel('body')
    ]
