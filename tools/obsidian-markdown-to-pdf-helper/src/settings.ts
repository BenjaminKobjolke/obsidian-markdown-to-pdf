import {App, PluginSettingTab, Setting} from "obsidian";
import MarkdownToPdfPlugin from "./main";

export interface PluginSettings {
	pythonToolPath: string;
	exportFolder: string;
}

export const DEFAULT_SETTINGS: PluginSettings = {
	pythonToolPath: '',
	exportFolder: ''
}

export class MarkdownToPdfSettingTab extends PluginSettingTab {
	plugin: MarkdownToPdfPlugin;

	constructor(app: App, plugin: MarkdownToPdfPlugin) {
		super(app, plugin);
		this.plugin = plugin;
	}

	display(): void {
		const {containerEl} = this;

		containerEl.empty();

		new Setting(containerEl)
			.setName('Python tool path')
			.setDesc('Path to the obsidian-markdown-to-pdf directory (where start.bat is located)')
			.addText(text => text
				.setPlaceholder('D:\\path\\to\\obsidian-markdown-to-pdf')
				.setValue(this.plugin.settings.pythonToolPath)
				.onChange(async (value) => {
					this.plugin.settings.pythonToolPath = value;
					await this.plugin.saveSettings();
				}));

		new Setting(containerEl)
			.setName('Export folder')
			.setDesc('Folder where exported PDFs are saved')
			.addText(text => text
				.setPlaceholder('D:\\path\\to\\pdf-exports')
				.setValue(this.plugin.settings.exportFolder)
				.onChange(async (value) => {
					this.plugin.settings.exportFolder = value;
					await this.plugin.saveSettings();
				}));
	}
}
